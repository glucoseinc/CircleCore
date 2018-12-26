# -*- coding: utf-8 -*-
"""他のCircleCoreとの同期.


Sequence:

```
participant Master as M
participant Slave as S
Note left of M: "HANDSHAKING" state
S->M: "hello" cmd
Note left of M: "MIGRATING" state
M->S: "migrate" cmd
S->M: "migrated" cmd
Note left of M: "SYNCING" state
M->S: "sync_message" cmds...
M->S: "new_message" cmds...
Note right of S: when Slave's circle core info is updated
S->M: "circle_core_updated" cmd
```

"""
import asyncio
import json
import logging
import uuid
from typing import Optional

from tornado.ioloop import IOLoop
from tornado.websocket import WebSocketHandler

from werkzeug import ImmutableDict

from circle_core.constants import MasterCommand, ReplicationState, SlaveCommand, WebsocketStatusCode
from circle_core.exceptions import ReplicationError
from circle_core.message import ModuleMessage, ModuleMessagePrimaryKey
from circle_core.models import CcInfo, MetaDataSession, ReplicationLink, ReplicationSlave

from ...helpers import make_message_topic
from ...models.message_box import MessageBox

logger = logging.getLogger(__name__)


class SyncState(object):
    box: MessageBox
    master_head: ModuleMessagePrimaryKey
    slave_head: Optional[ModuleMessagePrimaryKey]

    def __init__(self, box: MessageBox, master_head: ModuleMessagePrimaryKey):
        self.box = box
        self.master_head = master_head
        self.slave_head = None

    def is_synced(self):
        if self.slave_head is None:
            raise RuntimeError('sync state\'s slave status is not initialized.')
        return self.slave_head == self.master_head

    def __repr__(self):
        return '<SyncState box:{} master_head:{} slave_head:{}>'.format(
            self.box.uuid,
            self.master_head,
            self.slave_head,
        )


class ReplicationMasterHandler(WebSocketHandler):
    """スキーマを交換し、まだ相手に送っていないデータを送る.

    :param UUID slave_uuid:
    """

    def open(self, link_uuid):
        """他のCircleCoreから接続された際に呼ばれる."""
        logger.debug('%s Connected from slave CircleCore', link_uuid)
        self.link_uuid = link_uuid
        self.replication_link = ReplicationLink.query.get(link_uuid)

        if not self.replication_link:
            logger.warning('ReplicationLink %s was not found. Connection close.', link_uuid)
            self.close(
                code=WebsocketStatusCode.NOT_FOUND.value, reason='ReplicationLink {} was not found.'.format(link_uuid)
            )
            return

        database = self.get_core().get_database()
        self.state = ReplicationState.HANDSHAKING
        self.sync_states = ImmutableDict(
            (box.uuid, SyncState(box, database.get_latest_primary_key(box)))
            for box in self.replication_link.message_boxes
        )
        self.syncing = False
        logger.debug('initial sync status: %s', self.sync_states)

        # messageに関するイベントを監視する
        self.receiver = self.get_core().make_hub_receiver(make_message_topic())
        self.receiver.register_ioloop(self.on_new_message)

    def get_core(self):
        return self.application.settings['_core']

    async def on_message(self, plain_msg):
        """センサーからメッセージが送られてきた際に呼ばれる.

        {command: command from slave, ...payload}

        :param unicode plain_msg:
        """
        logger.debug('message from slave: %s' % plain_msg)
        json_msg = json.loads(plain_msg)

        try:
            command = SlaveCommand(json_msg['command'])
        except ValueError:
            raise ReplicationError('invalid command `{}`'.format(json_msg['command']))

        handler = getattr(self, 'on_slave_' + command.value)

        try:
            await handler(json_msg)
        except ReplicationError as exc:
            self.close(code=WebsocketStatusCode.VIOLATE_POLICY.value, reason=str(exc))

    def on_close(self):
        """センサーとの接続が切れた際に呼ばれる."""
        logger.debug('connection closed: %s', self)

        if hasattr(self, 'receiver'):  # Stop passing messages to slave
            IOLoop.current().remove_handler(self.receiver)

    def check_origin(self, origin):
        """CORSチェック."""
        # wsta等テストツールから投げる場合はTrueにしておく
        return True

    def _send_command(self, cmd, **kwargs):
        assert 'command' not in kwargs
        assert isinstance(cmd, MasterCommand)

        msg = kwargs.copy()
        msg['command'] = cmd.value
        raw = json.dumps(msg)
        return self.write_message(raw)

    async def on_slave_hello(self, json_msg):
        """hello コマンドが送られてきた"""
        assert self.state == ReplicationState.HANDSHAKING
        self.state = ReplicationState.MIGRATING

        # slave's cc info
        slave_info = json_msg['ccInfo']
        slave_uuid = uuid.UUID(slave_info['uuid'])

        with MetaDataSession.begin():
            # store slave's information
            if slave_uuid not in [slave.slave_uuid for slave in self.replication_link.slaves]:
                self.replication_link.slaves.append(
                    ReplicationSlave(link_uuid=self.replication_link.uuid, slave_uuid=slave_uuid)
                )

            cc_info = CcInfo.query.get(slave_uuid)
            if not cc_info:
                cc_info = CcInfo(uuid=slave_uuid, myself=False)
            cc_info.update_from_json(slave_info)
            MetaDataSession.add(cc_info)

        await self.send_migrate()

    def send_migrate(self):
        """共有対象のMessageBox関連データを配る"""

        message_boxes = self.replication_link.message_boxes
        modules = set(box.module for box in message_boxes)
        schemas = set(box.schema for box in message_boxes)

        return self._send_command(
            MasterCommand.MIGRATE,
            masterInfo=CcInfo.query.filter_by(myself=True).one().to_json(),
            messageBoxes=dict((str(obj.uuid), obj.to_json()) for obj in message_boxes),
            modules=dict((str(obj.uuid), obj.to_json()) for obj in modules),
            schemas=dict((str(obj.uuid), obj.to_json()) for obj in schemas),
        )

    async def on_slave_migrated(self, json_msg):
        """Slave側の受け入れ準備が整ったら送られてくる

        headsがslaveの最新データなのでそれ以降のデータを送る"""
        assert self.state == ReplicationState.MIGRATING
        self.state = ReplicationState.SYNCING

        database = self.get_core().get_database()
        conn = database.connect()

        # save slave head
        heads = json_msg.get('heads', {})
        for box in self.replication_link.message_boxes:
            sync_state = self.sync_states.get(box.uuid)
            sync_state.slave_head = ModuleMessagePrimaryKey.from_json(heads.get(str(box.uuid)))
            logger.debug('box: %s, slave head: %r', box.uuid, self.sync_states[box.uuid].slave_head)

        conn.close()

        self.syncing = True
        while True:
            logger.debug('syncing...')
            all_synced = await self.sync()
            if all_synced:
                break
            await asyncio.sleep(0.1)
        logger.debug('all synced')
        self.syncing = False

    async def sync(self):
        """master<>slave間で全boxを同期させようと試みる"""
        all_synced = True
        database = self.get_core().get_database()
        conn = database.connect()

        for box in self.replication_link.message_boxes:
            sync_state = self.sync_states[box.uuid]

            # logger.debug(
            #     'sync message box %s: from %s to %s', box.uuid,
            #     sync_state.slave_head,
            #     sync_state.master_head)
            count_messages = 0
            for message in database.enum_messages(box, head=self.sync_states[box.uuid].slave_head, connection=conn):
                logger.debug('sync message %s', message)
                await self._send_command(MasterCommand.SYNC_MESSAGE, message=message.to_json())
                sync_state.slave_head = message.primary_key
                count_messages += 1
            if count_messages == 0:
                # messageが0個の場合...
                logger.debug('%r has no messages!!', box.uuid)

            # logger.debug('  sync to %s', sync_state.slave_head)
            logger.debug('%r -> is_sycned %r', box.uuid, sync_state.is_synced())
            if not sync_state.is_synced():
                all_synced = False

        conn.close()
        return all_synced

    # Hub
    def on_new_message(self, topic, jsonobj):
        """新しいメッセージを受けとった"""
        message = ModuleMessage.from_json(jsonobj)
        logger.debug('on_new_message: %s', message)

        if message.box_id not in self.sync_states:
            # not target
            return
        sync_state = self.sync_states[message.box_id]

        try:
            if not sync_state.is_synced():
                # boxがまだsync中であればnew_messageは無視する。syncの方で同期されるはずなので
                logger.debug('skip message %s, because not synced', message)
                logger.debug(
                    '  master %s, slave %s', self.sync_states[message.box_id].master_head,
                    self.sync_states[message.box_id].slave_head
                )
            else:
                sync_state.slave_head = message.primary_key

                # pass to slave
                logger.debug('pass message %s', message)
                self._send_command(MasterCommand.NEW_MESSAGE, message=message.to_json())
        finally:
            sync_state.master_head = message.primary_key
