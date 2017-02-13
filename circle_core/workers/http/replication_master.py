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

from circle_core.constants import ReplicationState, SlaveCommand, MasterCommand, WebsocketStatusCode
from circle_core.exceptions import ReplicationError
from circle_core.models import CcInfo, MetaDataSession, NoResultFound, ReplicationLink
from ...exceptions import ModuleNotFoundError
# from ...helpers.metadata import metadata
from ...helpers import make_message_topic
# from ...helpers.topics import ModuleMessageTopic
from ...models.message_box import MessageBox


logger = logging.getLogger(__name__)


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
        self.is_box_synced = {}

        # messageに関するイベントを監視する
        logger.debug('open @ thread %r', threading.get_ident())
        self.receiver = self.get_core().make_hub_receiver(make_message_topic())
        self.receiver.set_timeout(10000)
        self.receiver.register_ioloop(self.on_new_message)

    def get_core(self):
        return self.application.settings['_core']

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

        future = handler(json_msg)
        logger.debug('future %r', future)

        def _done_callback(future):
            logger.debug(
                'on_slave_%s done : %r %r %r', command.value, future.done(), future.result(), future.exception())

        # future.add_done_callback(_done_callback)
        IOLoop.current().add_future(future, _done_callback)

        # logger.debug('on_slave_%s done', command.value)
        # if json_msg['command'] == 'MIGRATE':
        #     self.send_modules(json_msg['module_uuids'])
        # elif json_msg['command'] == 'RECEIVE':
        #     self.pass_messages()

        #     for box_uuid, value in json_msg['payload'].items():
        #         box = metadata().find_message_box(box_uuid)
        #         if box is not None:
        #             self.seed_messages(box, value['timestamp'], value['count'])

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
            cc_info = CcInfo(uuid=slave_uuid)
            cc_info.update_from_json(slave_info)

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

        heads = json_msg.get('heads', {})
        for box in self.replication_link.message_boxes:
            head = heads.get(str(box.uuid))
            # self.sync_message_box(box, head)

            # logger.info('box: %r, head: %r', box, head)

            # for message in database.enum_message_from(box, head=head, connection=conn):
            #     logger.info('sync message %s', message)
            #     self._send_command(
            #         MasterCommand.SYNC_MESSAGE,
            #         message=message.to_json()
            #     )

    # Hub
    def on_new_message(self, topic, message):
        """新しいメッセージを受けとった"""
        logger.debug('!? on_new_message %r %r', topic, message)
        return
# raw =
#
        box_id = request['box_id']
        payload = request['payload']

        from circle_core.models.replication_link import replcation_boxes_table

        try:
            message_box = MessageBox.query.filter(
                MessageBox.uuid == replcation_boxes_table.c.box_uuid,
                replcation_boxes_table.c.link_uuid == self.link_uuid,
            ).one()
        except NoResultFound:
            # not interested
            return

        self._send_command(
            MasterCommand.SYNC_MESSAGE,
            message=message.to_json()
        )

        return response

    # def seed_messages(self, box, since_timestamp, since_count):
    #     """蓄えたデータを共有.

    #     :param MessageBox box:
    #     :param int since_timestamp:
    #     :param int since_count:
    #     """
    #     for msg in box.messages_since(since_timestamp, since_count):
    #         logger.debug('Seeding already stored messages: %s', msg.encode())
    #         self.write_message(msg.encode())

    # def pass_messages(self):
    #     """自分がこれから受け取るメッセージを相手にも知らせるように."""
    #     def pass_message(msg):
    #         """自分がCircleModuleから受け取ったデータをslaveに垂れ流す.

    #         :param ModuleMessage msg:
    #         """
    #         if any(module.uuid == msg.module_uuid for module in self.subscribing_modules):
    #             logger.debug('Received from nanomsg: %s', msg.encode())
    #             self.write_message(msg.encode())

    #     logger.debug('Replication Master %s', ModuleMessageTopic().topic)
    #     self.receiver = Receiver(ModuleMessageTopic())
    #     self.receiver.register_ioloop(pass_message)
