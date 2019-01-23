# -*- coding: utf-8 -*-
"""nanomsgのhub."""

# system module
import asyncio
import os
import typing

# community module
from tornado.ioloop import IOLoop

# project module
from .base import logger
from ..helpers.nanomsg import Replier, Sender
from ..serialize import serialize

# type annotation
if typing.TYPE_CHECKING:
    from typing import Any, Awaitable, Callable, Dict, Optional, Union

    from ..types import Topic
    from ..message import ModuleMessage

    Request = Dict[str, Any]
    Response = Dict[str, Any]
    HandlerType = Callable[[Request], Union[Response, Awaitable[Response]]]


class HubError(Exception):
    """Hubに関する例外."""

    pass


class InvalidRequestError(HubError):
    """Requestが不正な場合の例外."""

    pass


class CoreHub(object):
    """nanomsgのPub/Subなどを管理するHub.

    request_socketでリクエストを待ち受けて、hub_socketのPub/Subに流す

    Attributes:
        message_handlers (Dict[str, Callable]): メッセージハンドラ
        hub_socket: nanomsgのメッセージが流通するHubのSocket
        request_socket (str): nanomsgへのリクエストを受け付けるSocket
        replier: リプライア
        sender: パブリッシャ
    """
    message_handlers: 'Dict[str, HandlerType]'
    replier: Replier
    sender: Sender

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

    def register_handler(self, name: str, handler: 'HandlerType'):
        """メッセージハンドラを登録する.

        :param str name: ハンドラ名
        :param Callable handler: ハンドラ
        """
        logger.info('register message handler: %s', name)
        self.message_handlers[name] = handler

    def publish(self, topic: 'Topic', message: 'ModuleMessage') -> None:
        """(topic, message)をPub/Subに送信する.

        :param str topic: topic名
        :param Dict message: Message
        """
        payload = topic.ljust(48) + serialize(message)
        self.sender.send(payload.encode('latin1'))

    # private
    async def handle_replier(self, request: 'Request', exception: 'Optional[Any]') -> None:
        """リプライアのハンドリング.

        Args:
            request: リクエスト
            exception: 例外発生時に格納されている
        """
        if exception:
            self.replier.send({'response': 'failed', 'message': str(exception)})
            return

        try:
            response = await self.handle_request(request)
        except Exception as exc:
            import traceback
            traceback.print_exc()
            response = {'response': 'failed', 'message': str(exc), 'original': request}

        self.replier.send(response)

    async def handle_request(self, request: 'Request') -> 'Response':
        """リクエストのハンドリング.

        :param Dict request: リクエスト
        :return: レスポンス
        :rtype: Dict
        """
        reqtype: str = request['request']

        if reqtype not in self.message_handlers:
            raise InvalidRequestError('Invalid request `{}`'.format(reqtype))

        handler = self.message_handlers[reqtype]
        # TODO: 全部coroutineにする
        if asyncio.iscoroutinefunction(handler):
            response = await typing.cast('Awaitable[Response]', handler(request))
        else:
            response = typing.cast('Response', handler(request))
        return response
