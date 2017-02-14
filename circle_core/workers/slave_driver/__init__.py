# -*- coding: utf-8 -*-
"""Master側のWebsocketの口とか、AdminのUIとか"""
import logging
import json
import uuid

# from websocket import create_connection, WebSocketConnectionClosedException
from tornado import gen
from tornado.websocket import websocket_connect

# project module
from circle_core.core.message import ModuleMessage
from circle_core.constants import ReplicationState, SlaveCommand, MasterCommand, WebsocketStatusCode
from circle_core.exceptions import ReplicationError
from circle_core.models import CcInfo, MetaDataSession, MessageBox, Module, NoResultFound, ReplicationMaster, Schema
from ..base import CircleWorker, register_worker_factory

logger = logging.getLogger(__name__)
WORKER_SLAVE_DRIVER = 'slave_driver'


@register_worker_factory(WORKER_SLAVE_DRIVER)
def create_slave_driver(core, type, key, config):
    assert type == WORKER_SLAVE_DRIVER

    return SlaveDriverWorker(
        core, key,
    )


class ConnectionClosed(Exception):
    def __init__(self, code, reason):
        self.code = WebsocketStatusCode(code) if code else None
        self.reason = reason

    def __repr__(self):
        return '<ConnectionClosed code={} reason={}>'.format(self.code, self.reason)


class DataConfilictedError(Exception):
    pass


class SlaveDriverWorker(CircleWorker):
    """
    """
    worker_type = WORKER_SLAVE_DRIVER

    def __init__(self, core, worker_key):
        super(SlaveDriverWorker, self).__init__(core, worker_key)

        self.replicators = []

    def initialize(self):
        for master in ReplicationMaster.query:
            self.start_replicator(master)

    def run(self):
        pass

    def finalize(self):
        for replicator in self.replicators:
            replicator.close()

    def start_replicator(self, master):
        replicator = Replicator(self, master)
        self.replicators.append(replicator)
        replicator.run()


class Replicator(object):
    def __init__(self, driver, master):
        self.driver = driver
        self.master = master
        self.ws = None
        self.target_boxes = None
        self.writer = None

        # fix url
        endpoint_url = master.endpoint_url
        if endpoint_url.startswith('http://'):
            endpoint_url = 'ws://' + endpoint_url[7:]
        elif endpoint_url.startswith('https://'):
            endpoint_url = 'wss://' + endpoint_url[8:]
        self.endpoint_url = endpoint_url

    @gen.coroutine
    def run(self):
        while True:
            try:
                yield self._run_one_loop()
            except ConnectionClosed as exc:
                logger.info('Replication connection was closed. code=%r, reason=%r', exc.code, exc.reason)

                if exc.code in (WebsocketStatusCode.CLOSE_NORMALY, WebsocketStatusCode.GOING_AWAY):
                    # 正常終了した場合はRetryする
                    logger.info('Replication connection was closed normarly. will retry after 5secs...')
                else:
                    # エラーコードが通知されている場合は、エラーを記録して終了する。復活するには再起動させること
                    logger.error(
                        'Replication connection was closed by peer. code=%r, reason=%r',
                        exc.code, exc.reason)
                    return
            except ConnectionRefusedError as exc:
                # 恐らく接続に失敗している > まだ立ち上がってない、のでWaitしてRetry
                logger.error(
                    'Replication connection was refused. %r',
                    exc)

            except Exception as exc:
                # エラーコードが通知されている場合は、エラーを記録して終了する。復活するには再起動させること
                logger.error(
                    'Replication connection was closed abnormaly. %r',
                    exc)
                import traceback
                traceback.print_exc()
                return
            finally:
                self.clear()

            # wait...
            yield gen.sleep(5.)

    def close(self):
        self.clear()

    def clear(self):
        if self.ws:
            self.ws.close()
        self.ws = None
        self.target_boxes = None
        self.writer = None

    @gen.coroutine
    def _run_one_loop(self):
        self.ws = yield websocket_connect(self.endpoint_url)
        self.state = ReplicationState.HANDSHAKING

        # HANDSHAKING
        self.send_hello_command()
        assert self.state == ReplicationState.MIGRATING
        yield self.wait_command(MasterCommand.MIGRATE)

        # MIGRATING
        self.send_migrated_command()
        assert self.state == ReplicationState.SYNCING
        while True:
            yield self.wait_command([MasterCommand.SYNC_MESSAGE, MasterCommand.NEW_MESSAGE])

    def _send_command(self, command, **payload):
        msg = {'command': command.value}
        msg.update(payload)
        self.ws.write_message(json.dumps(msg))

    def send_hello_command(self):
        """挨拶がてら自分の情報を送る。 対象CircleCoreじゃなければ接続が閉じられる"""
        assert self.state == ReplicationState.HANDSHAKING
        self.state = ReplicationState.MIGRATING

        myinfo = CcInfo.query.filter_by(myself=True).one()
        self._send_command(
            SlaveCommand.HELLO,
            ccInfo=myinfo.to_json()
        )

    def send_migrated_command(self):
        """Migrationが終わったので、自分のもっているMessageBoxのUUIDを送る"""
        assert self.state == ReplicationState.MIGRATING
        self.state = ReplicationState.SYNCING

        database = self.driver.core.get_database()
        # TODO: slave用のcycle設定をiniで制御できるようにする
        self.writer = database.make_writer()

        # 各MessageBoxのヘッドを取る
        heads = {}
        for box in self.target_boxes.values():
            pkey = database.get_latest_primary_key(box, connection=self.writer.connection)
            heads[str(box.uuid)] = pkey.to_json()

        self._send_command(
            SlaveCommand.MIGRATED,
            heads=heads,
        )

    @gen.coroutine
    def wait_command(self, commands):
        if not isinstance(commands, (list, tuple)):
            commands = (commands,)

        raw = yield self.ws.read_message()
        if raw is None:
            raise ConnectionClosed(self.ws.close_code, self.ws.close_reason)

        message = json.loads(raw)

        if message['command'] not in [c.value for c in commands]:
            raise ReplicationError('invalid command. want {}, but get {}'.format(commands, message['command']))

        handler = getattr(self, 'on_master_{}'.format(message['command']))
        handler(message)

    def on_master_migrate(self, message):
        assert self.state == ReplicationState.MIGRATING

        with MetaDataSession.begin():
            # save master info
            data = message['masterInfo']
            try:
                obj = CcInfo.query.filter_by(uuid=data['uuid']).one()
            except NoResultFound:
                obj = CcInfo(uuid=data['uuid'], myself=False)
            obj.update_from_json(data)
            obj.replication_master_id = self.master.id
            MetaDataSession.add(obj)

            master_info = obj

            # migrate schemas
            for schema_uuid, data in message['schemas'].items():
                try:
                    obj = Schema.query.filter_by(uuid=data['uuid']).one()
                except NoResultFound:
                    obj = Schema(uuid=data['uuid'])
                obj.update_from_json(data)
                obj.cc_uuid = master_info.uuid
                MetaDataSession.add(obj)

            # migrate modules
            for module_uuid, data in message['modules'].items():
                try:
                    obj = Module.query.filter_by(uuid=data['uuid']).one()
                except NoResultFound:
                    obj = Module(uuid=data['uuid'])
                obj.update_from_json(data)
                obj.cc_uuid = master_info.uuid
                MetaDataSession.add(obj)

            # migrate boxes
            self.target_boxes = {}
            for box_uuid, data in message['messageBoxes'].items():
                try:
                    obj = MessageBox.query.filter_by(uuid=data['uuid']).one()
                    if obj.schema_uuid != uuid.UUID(data['schemaUuid']):
                        raise DataConfilictedError('schemaUuid not match')
                    if obj.module_uuid != uuid.UUID(data['moduleUuid']):
                        raise DataConfilictedError('moduleUuid not match')
                except NoResultFound:
                    obj = MessageBox(
                        uuid=data['uuid'],
                        schema_uuid=data['schemaUuid'],
                        module_uuid=data['moduleUuid'],)
                obj.update_from_json(data)
                MetaDataSession.add(obj)

                self.target_boxes[obj.uuid] = obj

    def on_master_sync_message(self, message):
        assert self.state == ReplicationState.SYNCING
        self._store_message(message['message'])

    def on_master_new_message(self, message):
        assert self.state == ReplicationState.SYNCING
        self._store_message(message['message'])

    def _store_message(self, data):
        message = ModuleMessage.from_json(data)
        if message.box_id not in self.target_boxes:
            raise DataConfilictedError('invalid box id')

        message_box = MessageBox.query.filter_by(uuid=message.box_id).one()
        self.writer.store(message_box, message)
