# -*- coding: utf-8 -*-
"""nanomsgのhub."""

# system module
import os

# community module
from tornado.ioloop import IOLoop

# project module
from .base import logger
from ..helpers.nanomsg import Replier, Sender

# type annotation
try:
    from typing import Callable, Dict, Optional
except ImportError:
    pass


class HubError(Exception):
    """Hubに関する例外."""

    pass


class InvalidRequestError(HubError):
    """Requestが不正な場合の例外."""

    pass


class CoreHub(object):
    """nanomsgのPub/Subなどを管理するHub.

    request_socketでリクエストを待ち受けて、hub_socketのPub/Subに流す

    :param Dict[str, Callable] message_handlers: メッセージハンドラ
    :param str hub_socket: nanomsgのメッセージが流通するHubのSocket
    :param str request_socket: nanomsgへのリクエストを受け付けるSocket
    :param Sender sender: パブリッシャ
    :param Replier replier: リプライア
    """

    def __init__(self, hub_socket, request_socket):
        """init.

        :param str hub_socket: nanomsgのメッセージが流通するHubのSocket
        :param str request_socket: nanomsgへのリクエストを受け付けるSocket
        """
        self.message_handlers = {}
        self.hub_socket = hub_socket
        self.request_socket = request_socket

    def run(self):
        """Hubを起動する."""
        self.sender = Sender(self.hub_socket)
        self.replier = Replier(self.request_socket)
        self.replier.register_ioloop(self.handle_replier)

        logger.info('Hub running at PID:%s', os.getpid())
        IOLoop.current().start()

    def register_handler(self, name, handler):
        """メッセージハンドラを登録する.

        :param str name: ハンドラ名
        :param Callable handler: ハンドラ
        """
        logger.info('register message handler: %s', name)
        self.message_handlers[name] = handler

    def publish(self, topic, message):
        """(topic, message)をPub/Subに送信する.

        :param str topic: topic名
        :param Dict message: Message
        """
        self.sender.send(topic, message)

    # private
    def handle_replier(self, request, exception):
        """リプライアのハンドリング.

        :param Dict request: リクエスト
        :param Optional[Any] exception: 例外発生時に格納されている
        """
        if exception:
            self.replier.send({'response': 'failed', 'message': str(exception)})
            return

        try:
            response = self.handle_request(request)
        except Exception as exc:
            import traceback
            traceback.print_exc()
            response = {'response': 'failed', 'message': str(exc), 'original': request}

        self.replier.send(response)

    def handle_request(self, request):
        """リクエストのハンドリング.

        :param Dict request: リクエスト
        :return: レスポンス
        :rtype: Dict
        """
        reqtype = request['request']

        if reqtype not in self.message_handlers:
            raise InvalidRequestError('Invalid request `{}`'.format(reqtype))

        handler = self.message_handlers[reqtype]
        response = handler(request)
        return response
