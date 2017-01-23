# -*- coding: utf-8 -*-
"""TornadoでWebSocketサーバーを立てる."""
import json
import uuid

from tornado.websocket import WebSocketHandler

from circle_core.exceptions import CircleCoreException, ModuleNotFoundError
from circle_core.helpers.metadata import metadata
from circle_core.helpers.nanomsg import Sender
from circle_core.helpers.topics import ModuleMessageTopic
from circle_core.logger import get_stream_logger
from ...models.message import ModuleMessageFactory

logger = get_stream_logger(__name__)


class ModuleHandler(WebSocketHandler):
    """ここからワーカー達にnanomsg経由で命令を送る.

    接続毎にインスタンスが生成されている

    :param Module module:
    """

    def open(self, module_uuid):
        """センサーとの接続が開いた際に呼ばれる."""
        self.module = metadata().find_module(module_uuid)
        if not self.module:
            self.close(reason='Module not found')
            raise ModuleNotFoundError('module {} not found'.format(module_uuid))

        # TODO: 認証を行う
        # Senderはシングルトンだがインスタンス生成の直後にsendできないので予め作っておく
        self._sender = Sender(ModuleMessageTopic(self.module))
        logger.debug('connection opened: %s', self)

    def on_message(self, plain_msg):
        """センサーからメッセージが送られてきた際に呼ばれる.

        :param unicode msg:
        """
        logger.debug('Received from websocket: %s', plain_msg)

        json_msgs = json.loads(plain_msg)
        if not isinstance(json_msgs, list):
            json_msgs = [json_msgs]

        msgs_with_primary_key = []
        msgs_with_errors = []
        for json_msg in json_msgs:
            try:
                msgs_with_primary_key.append(ModuleMessageFactory.new(self.module.uuid, json_msg).encode())
            except CircleCoreException as exc:
                # TODO: エラーテーブルに追加する
                logger.error('Invalid message ({!r}). ignore it'.format(exc))
                msgs_with_errors.append((json_msg, exc))

        if msgs_with_primary_key:
            logger.debug('forwarind %d messages', len(msgs_with_primary_key))
            self._sender.send(msgs_with_primary_key)

    def on_close(self):
        """センサーとの接続が切れた際に呼ばれる."""
        logger.debug('connection closed: %s', self)

    def check_origin(self, origin):
        """CORSチェック."""
        # TODO: 本番環境でどうするか
        # wsta等テストツールから投げる場合はTrueにしておく
        return True
