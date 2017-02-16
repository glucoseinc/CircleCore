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
import enum
import json
import logging
import threading
import uuid

from click import get_current_context

from tornado import gen
from tornado.ioloop import IOLoop
from tornado.web import HTTPError
from tornado.websocket import WebSocketHandler
from werkzeug import ImmutableDict

from circle_core.constants import MasterCommand, ReplicationState, SlaveCommand, WebsocketStatusCode
from circle_core.exceptions import ReplicationError
from circle_core.message import ModuleMessage, ModuleMessagePrimaryKey
from circle_core.models import CcInfo, MetaDataSession, NoResultFound, ReplicationLink
from ...exceptions import ModuleNotFoundError
# from ...helpers.metadata import metadata
from ...helpers import make_message_topic
# from ...helpers.topics import ModuleMessageTopic
from ...models.message_box import MessageBox


logger = logging.getLogger(__name__)


class SyncState(object):
    def __init__(self, box):
        self.box = box
        self.slave_head = None
        self.master_head = None

    def is_synced(self):
        return self.slave_head == self.master_head


class ReplicationMaster(WebSocketHandler):
    """スキーマを交換し、まだ相手に送っていないデータを送る.

    :param UUID slave_uuid:
    """

    def open(self, link_uuid):
        """他のCircleCoreから接続された際に呼ばれる."""
        logger.debug('Connected to another CircleCore')
        self.link_uuid = link_uuid
        self.replication_link = ReplicationLink.query.get(link_uuid)

        if not self.replication_link:
            raise HTTPError(404)

        self.state = ReplicationState.HANDSHAKING
        self.sync_states = ImmutableDict(
            (box.uuid, SyncState(box)) for box in self.replication_link.message_boxes
        )

        # get master heads
        database = self.get_core().get_database()
        conn = database.connect()
        for box_uuid, sync_state in self.sync_states.items():
            head = database.get_latest_primary_key(sync_state.box, connection=conn)
            sync_state.master_head = head

        # messageに関するイベントを監視する
        self.receiver = self.get_core().make_hub_receiver(make_message_topic())
        self.receiver.register_ioloop(self.on_new_message)

    def get_core(self):
        return self.application.settings['_core']

    @gen.coroutine
    def on_message(self, plain_msg):
        """センサーからメッセージが送られてきた際に呼ばれる.

        {
            command: command from slave
            ...payload
        }

        :param unicode message:
        """
        logger.debug('message from slave: %s' % plain_msg)
        json_msg = json.loads(plain_msg)

        try:
            command = SlaveCommand(json_msg['command'])
        except ValueError:
            raise ReplicationError('invalid command `{}`'.format(json_msg['command']))

        handler = getattr(self, 'on_slave_' + command.value)

        try:
            yield handler(json_msg)
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

    @gen.coroutine
    def on_slave_hello(self, json_msg):
        """hello コマンドが送られてきた"""
        assert self.state == ReplicationState.HANDSHAKING
        self.state = ReplicationState.MIGRATING

        # slave's cc info
        slave_info = json_msg['ccInfo']
        slave_uuid = uuid.UUID(slave_info['uuid'])

        if slave_uuid not in [s.slave_uuid for s in self.replication_link.slaves]:
            logger.error('core %r not allowed', slave_uuid)
            raise ReplicationError('core {} not allowed'.format(slave_uuid))

        with MetaDataSession.begin():
            # store slave's information
            cc_info = CcInfo.query.get(slave_uuid)
            if not cc_info:
                cc_info = CcInfo(uuid=slave_uuid, myself=False)
            cc_info.update_from_json(slave_info)
            MetaDataSession.add(cc_info)

        yield self.send_migrate()

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

    @gen.coroutine
    def on_slave_migrated(self, json_msg):
        """Slave側の受け入れ準備が整ったら送られてくる

        headsがslaveの最新データなのでそれ以降のデータを送る"""
        assert self.state == ReplicationState.MIGRATING
        self.state = ReplicationState.SYNCING

        database = self.get_core().get_database()
        conn = database.connect()

        try:
            heads = json_msg.get('heads', {})
            for box in self.replication_link.message_boxes:
                head = ModuleMessagePrimaryKey.from_json(heads.get(str(box.uuid)))
                logger.info('box: %r, head: %r', box, head)
                self.sync_states[box.uuid].slave_head = head

                for message in database.enum_messages(box, head=head, connection=conn):
                    logger.debug('sync message %s', message)
                    self._send_command(
                        MasterCommand.SYNC_MESSAGE,
                        message=message.to_json()
                    )
                    self.sync_states[box.uuid].slave_head = message.primary_key
                logger.info('box: %r synced', box)
        except:
            import traceback
            traceback.print_exc()
            raise
        finally:
            conn.close()

    # Hub
    def on_new_message(self, topic, jsonobj):
        """新しいメッセージを受けとった"""
        message = ModuleMessage.from_json(jsonobj)

        if message.box_id not in self.sync_states:
            # not interested
            return

        sync_state = self.sync_states[message.box_id]
        if sync_state.is_synced():
            # pass to slave
            logger.debug('pass message %s', message)
            self._send_command(
                MasterCommand.NEW_MESSAGE,
                message=message.to_json()
            )
            sync_state.slave_head = message.primary_key
        sync_state.master_head = message.primary_key
