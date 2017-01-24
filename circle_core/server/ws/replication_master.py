# -*- coding: utf-8 -*-
"""他のCircleCoreとの同期."""
import json
from uuid import UUID

from tornado.ioloop import IOLoop
from tornado.websocket import WebSocketHandler

from ...exceptions import ModuleNotFoundError
from ...helpers.metadata import metadata
from ...helpers.nanomsg import Receiver
from ...helpers.topics import ModuleMessageTopic
from ...logger import get_stream_logger
from ...models.message_box import MessageBox


logger = get_stream_logger(__name__)


class ReplicationMaster(WebSocketHandler):
    """スキーマを交換し、まだ相手に送っていないデータを送る.

    :param UUID slave_uuid:
    """

    def open(self, slave_uuid):
        """他のCircleCoreから接続された際に呼ばれる."""
        logger.debug('Connected to another CircleCore')
        self.slave_uuid = slave_uuid

    def on_message(self, plain_msg):
        """センサーからメッセージが送られてきた際に呼ばれる.

        :param unicode message:
        """
        json_msg = json.loads(plain_msg)
        if json_msg['command'] == 'MIGRATE':
            self.send_modules(json_msg['module_uuids'])
        elif json_msg['command'] == 'RECEIVE':
            self.pass_messages()

            for box_uuid, value in json_msg['payload'].items():
                box = metadata().find_message_box(box_uuid)
                if box is not None:
                    self.seed_messages(box, value['timestamp'], value['count'])

        logger.debug('message from another circlecore: %r' % json_msg)

    def on_close(self):
        """センサーとの接続が切れた際に呼ばれる."""
        logger.debug('connection closed: %s', self)

        if hasattr(self, 'receiver'):  # Stop passing messages to slave
            IOLoop.current().remove_handler(self.receiver)

    def check_origin(self, origin):
        """CORSチェック."""
        # wsta等テストツールから投げる場合はTrueにしておく
        return True

    def send_modules(self, module_uuids):
        """自分に登録されているDataSourceとSchemaを通知."""
        self.subscribing_modules = [
            module
            for module in map(metadata().find_module, module_uuids)
            if module is not None
        ]
        boxes = [
            metadata().find_message_box(box_uuid)
            for module in self.subscribing_modules
            for box_uuid in module.message_box_uuids
        ]
        schemas = [metadata().find_schema(box.schema_uuid) for box in boxes]
        resp = json.dumps({
            'modules': [module.to_json() for module in self.subscribing_modules if not module.of_master],
            'message_boxes': [box.to_json() for box in boxes if not box.of_master],
            'schemas': [schema.to_json() for schema in schemas if not schema.of_master]
        })
        self.write_message(resp)

    def seed_messages(self, box, since_timestamp, since_count):
        """蓄えたデータを共有.

        :param MessageBox box:
        :param int since_timestamp:
        :param int since_count:
        """
        for msg in box.messages_since(since_timestamp, since_count):
            logger.debug('Seeding already stored messages: %s', msg.encode())
            self.write_message(msg.encode())

    def pass_messages(self):
        """自分がこれから受け取るメッセージを相手にも知らせるように."""
        def pass_message(msg):
            """自分がCircleModuleから受け取ったデータをslaveに垂れ流す.

            :param ModuleMessage msg:
            """
            if any(module.uuid == msg.module_uuid for module in self.subscribing_modules):
                logger.debug('Received from nanomsg: %s', msg.encode())
                self.write_message(msg.encode())

        logger.debug('Replication Master %s', ModuleMessageTopic().topic)
        self.receiver = Receiver(ModuleMessageTopic())
        self.receiver.register_ioloop(pass_message)
