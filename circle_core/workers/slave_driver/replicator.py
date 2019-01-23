# -*- coding: utf-8 -*-

# system module
import asyncio
import functools
import json
import logging
import typing
import uuid

# community module
from tornado import httpclient
from tornado.websocket import WebSocketError, websocket_connect

# project module
from circle_core.constants import MasterCommand, ReplicationState, SlaveCommand, WebsocketStatusCode
from circle_core.exceptions import ReplicationError
from circle_core.message import ModuleMessage, ModuleMessagePrimaryKey
from circle_core.models import CcInfo, MessageBox, MetaDataSession, Module, NoResultFound, Schema

if typing.TYPE_CHECKING:
    from typing import Dict, Optional, Tuple

    from circle_core.writer import QueuedDBWriter
    from . import SlaveDriverWorker
    from ..models import ReplicationMaster

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

    Attributes:
        driver (SlaveDriverWorker):
        master (circle_core.models.ReplicationMaster):
        ws (Optional[WebSocketClientConnection]):
        closed (bool):
        endpoint_url (str):
    """
    driver: 'SlaveDriverWorker'
    master: 'ReplicationMaster'
    target_boxes: 'Optional[Dict[uuid.UUID, MessageBox]]'
    writer: 'Optional[QueuedDBWriter]'

    def __init__(self, driver: 'SlaveDriverWorker', master: 'ReplicationMaster', request_options=None):
        self.driver = driver
        self.master = master
        self.ws = None
        self.target_boxes = None
        self.writer = None
        self.closed = False
        self.request_options = request_options or {}
        self.runner = None

        # fix url
        endpoint_url = master.endpoint_url
        if endpoint_url.startswith('http://'):
            endpoint_url = 'ws://' + endpoint_url[7:]
        elif endpoint_url.startswith('https://'):
            endpoint_url = 'wss://' + endpoint_url[8:]
        self.endpoint_url = endpoint_url

    def run(self):
        self.runner = asyncio.ensure_future(self.run_async())

    def close(self):
        assert self.runner
        self.closed = True
        asyncio.get_event_loop().run_until_complete(asyncio.wait_for(self.runner, None))
        self.clear()

    async def close_async(self):
        assert self.runner
        self.closed = True
        await asyncio.wait_for(self.runner, None)
        self.clear()

    # private
    async def run_async(self):
        if not (self.endpoint_url.startswith('ws://') or self.endpoint_url.startswith('wss://')):
            logger.info('Invalid replication link: `%s`, replicator closed', self.endpoint_url)
            return

        while not self.closed:
            try:
                await self._run_one_loop()
            except ConnectionClosed as exc:
                logger.info('Replication connection was closed. code=%r, reason=%r', exc.code, exc.reason)

                if exc.code in (WebsocketStatusCode.CLOSE_NORMALLY, WebsocketStatusCode.GOING_AWAY):
                    # 正常終了した場合はRetryする
                    logger.info('Replication connection was closed normally. will retry after 5secs...')
                elif exc.code:
                    # エラーコードが通知されている場合は、エラーを記録して終了する。復活するには再起動させること
                    logger.error('Replication connection was closed by peer. code=%r, reason=%r', exc.code, exc.reason)
                    return
                elif not self.closed:
                    # エラーコードなし。おそらくMasterが終了した
                    logger.info('Replication connection was closed abnormally by peer. will retry after 5secs...')

            except ConnectionRefusedError:
                # 恐らく接続に失敗している > まだ立ち上がってない、のでWaitしてRetry
                logger.exception('Replication connection was refused. %r')

            except WebSocketError:
                # WebSocket上のエラーの場合は、エラーを記録して終了する。復活するには再起動させること
                logger.exception('Replication connection was closed abnormally.')
                return

            except Exception:
                # その他のエラーは、エラーを記録、TraceBackを表示して終了する。復活するには再起動させること
                logger.exception('Replication connection was closed abnormally.')
                return
            finally:
                self.clear()

            # wait...
            if not self.closed:
                await asyncio.sleep(5.)

        logger.info('Replicator closed (%s)', self.endpoint_url)

    def clear(self):
        if self.ws:
            self.ws.close()
        if self.writer:
            asyncio.get_event_loop().run_until_complete(functools.partial(self.writer.flush, flush_all=True))

        self.target_boxes = None
        self.writer = None
        self.runner = None

    async def _run_one_loop(self):
        # make request
        request = httpclient.HTTPRequest(self.endpoint_url, **self.request_options)

        # make connection
        self.ws = await websocket_connect(request)
        self.state = ReplicationState.HANDSHAKING

        logger.info('Replication connection to %s: established', self.endpoint_url)

        # HANDSHAKING
        self.send_hello_command()
        assert self.state == ReplicationState.MIGRATING
        await self.wait_command((MasterCommand.MIGRATE,))

        # MIGRATING
        self.send_migrated_command()
        assert self.state == ReplicationState.SYNCING

        logger.info('Replication connection to %s: migrated, start syncing', self.endpoint_url)

        while not self.closed:
            await self.wait_command((MasterCommand.SYNC_MESSAGE, MasterCommand.NEW_MESSAGE))

    def _send_command(self, command: MasterCommand, **payload):
        if self.ws is None:
            ReplicationError('Websocket is not connected')
        else:
            ws = self.ws

        msg = {'command': command.value}
        msg.update(payload)
        ws.write_message(json.dumps(msg))

    def send_hello_command(self):
        """挨拶がてら自分の情報を送る。 対象CircleCoreじゃなければ接続が閉じられる"""
        assert self.state == ReplicationState.HANDSHAKING
        self.state = ReplicationState.MIGRATING

        myinfo = CcInfo.query.filter_by(myself=True).one()
        self._send_command(SlaveCommand.HELLO, ccInfo=myinfo.to_json())

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
            pkey = database.get_latest_primary_key(box)
            if pkey is None:  # メッセージボックスが空だったら
                heads[str(box.uuid)] = ModuleMessagePrimaryKey.origin().to_json()
            else:
                heads[str(box.uuid)] = pkey.to_json()

        self._send_command(
            SlaveCommand.MIGRATED,
            heads=heads,
        )

    async def wait_command(self, commands: 'Tuple[ReplicationState, ...]') -> None:
        """commandsで指定したコマンドが来るまで待つ

        違うコマンドが来たらReplicationError例外を起こす
        """
        if self.ws is None:
            ReplicationError('Websocket is not connected')
        else:
            ws = self.ws

        raw = await ws.read_message()
        if raw is None:
            raise ConnectionClosed(ws.close_code, ws.close_reason)

        message = json.loads(raw)

        if message['command'] not in [c.value for c in commands]:
            raise ReplicationError('invalid command. want {}, but get {}'.format(commands, message['command']))

        handler = getattr(self, 'on_master_{}'.format(message['command']))
        await handler(message)

    async def on_master_migrate(self, message):
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
                        module_uuid=data['moduleUuid'],
                    )
                obj.update_from_json(data)
                MetaDataSession.add(obj)

                self.target_boxes[obj.uuid] = obj

    async def on_master_sync_message(self, message):
        assert self.state == ReplicationState.SYNCING
        await self._store_message(message['message'])

    async def on_master_new_message(self, message):
        assert self.state == ReplicationState.SYNCING
        await self._store_message(message['message'])

    async def _store_message(self, data):
        logger.info('!?data', repr(data))
        message = ModuleMessage.from_json(data)
        logger.info('!?message', repr(message))
        if message.box_id not in self.target_boxes:
            raise DataConfilictedError('invalid box id')

        message_box = MessageBox.query.filter_by(uuid=message.box_id).one()
        await self.writer.store(message_box, message)
