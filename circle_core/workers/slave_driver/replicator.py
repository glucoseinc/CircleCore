# -*- coding: utf-8 -*-

# system module
import json
import logging
import uuid

# community module
from six import PY3
from tornado import gen
from tornado.websocket import websocket_connect, WebSocketClientConnection

# project module
from circle_core.constants import MasterCommand, ReplicationState, SlaveCommand, WebsocketStatusCode
from circle_core.database import QueuedWriter
from circle_core.exceptions import ReplicationError
from circle_core.message import ModuleMessage, ModuleMessagePrimaryKey
from circle_core.models import CcInfo, MessageBox, MetaDataSession, Module, NoResultFound, ReplicationMaster, Schema

if PY3:
    from typing import Dict, Optional


logger = logging.getLogger(__name__)


# exceptions for internal use
class ConnectionClosed(Exception):
    def __init__(self, code, reason):
        self.code = WebsocketStatusCode(code) if code else None
        self.reason = reason

    def __repr__(self):
        return '<ConnectionClosed code={} reason={}>'.format(self.code, self.reason)


class DataConfilictedError(Exception):
    pass


# Replicator
class Replicator(object):
    """Replicator.

    :param SlaveDriverWorker driver:
    :param ReplicationMaster master:
    :param Optional[WebSocketClientConnection] ws:
    :param Optional[Dict[uuid.UUID, MessageBox]] target_boxes:
    :param Optional[QueuedWriter] writer:
    :param bool closed:
    :param str endpoint_url:
    """

    def __init__(self, driver, master):
        self.driver = driver
        self.master = master
        self.ws = None
        self.target_boxes = None
        self.writer = None
        self.closed = False

        # fix url
        endpoint_url = master.endpoint_url
        if endpoint_url.startswith('http://'):
            endpoint_url = 'ws://' + endpoint_url[7:]
        elif endpoint_url.startswith('https://'):
            endpoint_url = 'wss://' + endpoint_url[8:]
        self.endpoint_url = endpoint_url

    @gen.coroutine
    def run(self):
        if not (self.endpoint_url.startswith('ws://') or self.endpoint_url.startswith('wss://')):
            logger.info('Invalid replication link: `%s`, replicator closed', self.endpoint_url)
            return

        while not self.closed:
            try:
                yield self._run_one_loop()
            except ConnectionClosed as exc:
                logger.info('Replication connection was closed. code=%r, reason=%r', exc.code, exc.reason)

                if exc.code in (WebsocketStatusCode.CLOSE_NORMALLY, WebsocketStatusCode.GOING_AWAY):
                    # 正常終了した場合はRetryする
                    logger.info('Replication connection was closed normarly. will retry after 5secs...')
                elif exc.code:
                    # エラーコードが通知されている場合は、エラーを記録して終了する。復活するには再起動させること
                    logger.error(
                        'Replication connection was closed by peer. code=%r, reason=%r',
                        exc.code, exc.reason)
                    return
                elif not self.closed:
                    # エラーコードなし。おそらくMasterが終了した
                    logger.info('Replication connection was closed abnormaly by peer. will retry after 5secs...')

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
            if not self.closed:
                yield gen.sleep(5.)

        logger.info('Replicator closed (%s)', self.endpoint_url)

    def close(self):
        self.closed = True
        self.clear()

    def clear(self):
        if self.ws:
            self.ws.close()
        if self.writer:
            self.writer.commit(flush_all=True)

        self.target_boxes = None
        self.writer = None

    @gen.coroutine
    def _run_one_loop(self):
        self.ws = yield websocket_connect(self.endpoint_url)
        self.state = ReplicationState.HANDSHAKING

        logger.info('Replication connection to %s: established', self.endpoint_url)

        # HANDSHAKING
        self.send_hello_command()
        assert self.state == ReplicationState.MIGRATING
        yield self.wait_command(MasterCommand.MIGRATE)

        # MIGRATING
        self.send_migrated_command()
        assert self.state == ReplicationState.SYNCING

        logger.info('Replication connection to %s: migrated, start syncing', self.endpoint_url)

        while not self.closed:
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
            if pkey is None:  # メッセージボックスが空だったら
                heads[str(box.uuid)] = ModuleMessagePrimaryKey.origin().to_json()
            else:
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

            self.master.master_uuid = master_info.uuid

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
                obj.replication_master_id = self.master.id
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
