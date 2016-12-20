# -*- coding: utf-8 -*-
"""他のCircleCoreとの同期."""
import json

from tornado.ioloop import IOLoop
from tornado.websocket import WebSocketHandler

from ...helpers.nanomsg import Receiver
from ...helpers.topics import SensorDataTopic
from ...logger import get_stream_logger

logger = get_stream_logger(__name__)


class ReplicationHandler(WebSocketHandler):
    """スキーマを交換し、まだ相手に送っていないデータを送る

    :param Sender __nanomsg:
    """

    def open(self, slave_uuid):
        """他のCircleCoreから接続された際に呼ばれる."""
        logger.debug('Connected to another CircleCore')
        self.slave_uuid = slave_uuid

    def on_message(self, msg):
        """センサーからメッセージが送られてきた際に呼ばれる.

        :param unicode message:
        """
        action = json.loads(msg)
        if action['command'] == 'MIGRATE':
            self.send_modules()
        elif action['command'] == 'RETRIEVE':
            self.pass_messages()

        logger.debug('message from another circlecore: %r' % msg)

    def on_close(self):
        """センサーとの接続が切れた際に呼ばれる."""
        logger.debug('connection closed: %s', self)

        if hasattr(self, 'watching_fd'):
            IOLoop.current().remove_handler(self.watching_fd)

    def check_origin(self, origin):
        """CORSチェック."""
        # wsta等テストツールから投げる場合はTrueにしておく
        return True

    def send_modules(self):
        """自分に登録されているDataSourceとSchemaを通知."""
        metadata = self.application.settings['cr_metadata']
        modules = [
            {
                'display_name': module.display_name,
                'uuid': module.uuid.hex,
                'schema_uuid': module.schema_uuid.hex,
                'properties': module.stringified_properties
            } for module in metadata.modules
        ]
        schemas = [
            {
                'display_name': schema.display_name,
                'uuid': schema.uuid.hex,
                'properties': schema.stringified_properties
            } for schema in metadata.schemas
        ]
        resp = json.dumps({'modules': modules, 'schemas': schemas})
        self.write_message(resp)

    def pass_messages(self):
        """自分がこれから受け取るメッセージを相手にも知らせるように."""
        def pass_message(decoded):
            module_uuid, payload = decoded
            resp = json.dumps({
                'module': module_uuid.hex,
                'payload': payload
            })
            self.write_message(resp)

        self.watching_fd = Receiver().register_ioloop(SensorDataTopic(), pass_message)
