# -*- coding: utf-8 -*-
"""TornadoでWebSocketサーバーを立てる."""

from tornado.websocket import WebSocketHandler

from circle_core.exceptions import ModuleNotFoundError
from circle_core.helpers.nanomsg import Sender
from circle_core.helpers.topics import SensorDataTopic
from circle_core.logger import get_stream_logger

logger = get_stream_logger(__name__)


class SensorHandler(WebSocketHandler):
    """ここからワーカー達にnanomsg経由で命令を送る.

    接続毎にインスタンスが生成されている
    """

    def open(self, module_uuid):
        """センサーとの接続が開いた際に呼ばれる."""
        # TODO: cr_metadata周りは作り直す
        module = self.application.settings['cr_metadata'].find_module(module_uuid)
        if not module:
            raise ModuleNotFoundError('module {} not found'.format(module_uuid))

        # TODO: 認証を行う
        # Senderはシングルトンだがインスタンス生成の直後にsendできないので予め作っておく
        self._sender = Sender(SensorDataTopic(module))
        logger.debug('connection opened: %s', self)

    def on_message(self, msg):
        """センサーからメッセージが送られてきた際に呼ばれる.

        :param unicode msg:
        """
        logger.debug('Received from nanomsg: %s', msg)
        rv = self._sender.send(msg)
        logger.debug('%r', rv)

    def on_close(self):
        """センサーとの接続が切れた際に呼ばれる."""
        logger.debug('connection closed: %s', self)

    def check_origin(self, origin):
        """CORSチェック."""
        # FIXME: 本番環境でどうするか
        # wsta等テストツールから投げる場合はTrueにしておく
        return True
