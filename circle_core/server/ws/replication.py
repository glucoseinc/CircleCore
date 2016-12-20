# -*- coding: utf-8 -*-
"""他のCircleCoreとの同期."""
import json

from tornado.websocket import WebSocketHandler

from ...helpers.topics import SensorDataTopic
from ...helpers.nanomsg import Receiver
from ...logger import get_stream_logger

logger = get_stream_logger(__name__)


class ReplicationHandler(WebSocketHandler):
    """スキーマを交換し、まだ相手に送っていないデータを送る

    :param Sender __nanomsg:
    """

    def open(self):
        """他のCircleCoreから接続された際に呼ばれる."""
        logger.debug('Connected to another CircleCore')

    def on_message(self, msg):
        """センサーからメッセージが送られてきた際に呼ばれる.

        :param unicode message:
        """
        action = json.loads(msg)
        if action['type'] == 'HANDSHAKE':
            self.handshake()
        elif action['type'] == 'READY':
            self.ready()

        logger.debug('message from another circlecore: %r' % msg)

    def on_close(self):
        """センサーとの接続が切れた際に呼ばれる."""
        logger.debug('connection closed: %s', self)

    def check_origin(self, origin):
        """CORSチェック."""
        # wsta等テストツールから投げる場合はTrueにしておく
        return True

    def handshake(self):
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

    def ready(self):
        """自分がこれから受け取るメッセージを相手にも知らせるように."""
        def pass_message(decoded):
            module_uuid, payload = decoded
            resp = json.dumps({
                'module': module_uuid.hex,
                'payload': payload
            })
            self.write_message(resp)

        Receiver().register_ioloop(SensorDataTopic(), pass_message)
