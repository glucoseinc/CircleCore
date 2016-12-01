# -*- coding: utf-8 -*-
"""TornadoでWebSocketサーバーを立てる."""
from logging import getLogger

from tornado.websocket import WebSocketHandler

from circle_core.exceptions import DeviceNotFoundError
from circle_core.helpers.nanomsg import Sender
from circle_core.helpers.topics import SensorDataTopic

logger = getLogger(__name__)


class SensorHandler(WebSocketHandler):
    """ここからワーカー達にnanomsg経由で命令を送る.

    接続毎にインスタンスが生成されている

    :param Sender __nanomsg:
    """

    def open(self, device_uuid):
        """センサーとの接続が開いた際に呼ばれる."""
        # Senderはシングルトンだが今のところインスタンス生成の直後にsendできないので予め作っておく

        # TODO: cr_config周りは作り直す
        device = self.application.settings['cr_config'].find_device(device_uuid)
        if not device:
            raise DeviceNotFoundError('device {} not found'.format(device_uuid))

        # TODO: 認証を行う

        self.topic = SensorDataTopic(device)
        self.__sender = Sender()
        logger.debug('connection opened: %s', self)

    def on_message(self, message):  # TODO: messageのスキーマを決める
        """センサーからメッセージが送られてきた際に呼ばれる.

        :param unicode message:
        """
        rv = self.__sender.send(self.topic.with_json(message))
        logger.debug('%r', rv)
        logger.debug('message %r is sent from %s with topic %r', message, self, self.topic.topic)

    def on_close(self):
        """センサーとの接続が切れた際に呼ばれる."""
        logger.debug('connection closed: %s', self)

    def check_origin(self, origin):
        """CORSチェック."""
        # wsta等テストツールから投げる場合はTrueにしておく
        return True
