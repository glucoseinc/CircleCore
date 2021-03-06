# -*- coding: utf-8 -*-
"""nanomsgのラッパー."""

# system module
import asyncio
import json
import logging
import typing
from typing import Awaitable, Callable, cast

# community module
import nnpy

from tornado.ioloop import IOLoop

# project module
from .topics import TOPIC_LENGTH

# type annotation
if typing.TYPE_CHECKING:
    pass

__all__ = (
    'Receiver',
    'Sender',
    'Replier',
)
logger = logging.getLogger(__name__)

RawMessage = typing.TypeVar('RawMessage')
ReplierCallback = Callable[[RawMessage, Exception], Awaitable[None]]


class Receiver(object):
    """受信. PubSubのSub.

    :param nnpy.Socket _socket: nanomsg Socket
    :param str topic: topic名
    """

    def __init__(self, socket_url, topic=None):
        """init.

        接続を開く.

        :param str socket_url: socketのURI
        :param str topic: topic名
        """
        self._socket = nnpy.Socket(nnpy.AF_SP, nnpy.SUB)
        self._socket.connect(socket_url)
        if topic:
            self._socket.setsockopt(nnpy.SUB, nnpy.SUB_SUBSCRIBE, topic.rstrip())
        self.topic = topic

    def __del__(self):
        """del.

        接続を閉じる.
        """
        self._socket.close()

    def fileno(self):
        """Tornadoに叩かれる."""
        hoge = self._socket.getsockopt(nnpy.SOL_SOCKET, nnpy.RCVFD)
        return hoge

    def close(self):
        """Tornadoに叩かれる."""
        logger.debug('close')
        self._socket.close()

    def set_timeout(self, timeout):
        """タイムアウトを設定する.

        :param int timeout: タイムアウト millisecond
        """
        self._socket.setsockopt(nnpy.SOL_SOCKET, nnpy.RCVTIMEO, timeout)

    def register_ioloop(self, callback):
        """TornadoのIOLoopにメッセージ受信時のコールバックを登録.

        :param FunctionType callback:
        """

        def call_callback_receiver(*args):
            # TODO: topicを設定している場合、違うTopicのパケットがきてもpollが反応するのでdontwaitにしてチェックしないといけないかも
            try:
                raw = self._socket.recv()
                plain_msg = raw.decode('utf-8')
                topic, message = plain_msg[:TOPIC_LENGTH], plain_msg[TOPIC_LENGTH:]
                message = json.loads(message)
                rv = callback(topic, message)

                if asyncio.iscoroutine(rv):
                    # fire and forget
                    asyncio.ensure_future(rv)

            except Exception:
                import traceback
                traceback.print_exc()

        IOLoop.current().add_handler(self, call_callback_receiver, IOLoop.READ)


class Sender(object):
    """送信. PubSubのPub.

    同じアドレスにbindできるのは一度に一つのSocketだけなのでSingleton.

    :param nnpy.Socket _socket:
    """

    def __init__(self, socket_url):
        """init.

        接続を開く.

        :param str socket_url: socketのURI
        """
        self._socket = nnpy.Socket(nnpy.AF_SP, nnpy.PUB)
        self._socket.bind(socket_url)
        # TODO: bindの名前解決がasyncで行われるはずなので、それをスマートに待機する方法を調べておく

    def __del__(self):
        """del.

        接続を閉じる.
        """
        self._socket.close()

    def send(self, payload: bytes) -> None:
        """送信.

        :param str topic: topic名
        :param Dict payload: payload
        """
        self._socket.send(payload)


class Replier(object):

    def __init__(self, socket_url):
        """init.

        接続を開く.

        :param str socket_url: socketのURI
        """
        self._socket = nnpy.Socket(nnpy.AF_SP, nnpy.REP)
        self._socket.bind(socket_url)
        # TODO: bindの名前解決がasyncで行われるはずなので、それをスマートに待機する方法を調べておく

    def __del__(self):
        """del.

        接続を閉じる.
        """
        self._socket.close()

    def recv(self) -> RawMessage:
        """受信."""
        raw = self._socket.recv()
        return cast(RawMessage, json.loads(raw.decode('utf-8')))

    def send(self, payload: RawMessage):
        """送信.

        :param Dict payload: payload
        """
        data = json.dumps(payload)
        return self._socket.send(data.encode('utf-8'))

    def fileno(self):
        """Tornadoに叩かれる."""
        return self._socket.getsockopt(nnpy.SOL_SOCKET, nnpy.RCVFD)

    def close(self) -> None:
        """Tornadoに叩かれる."""
        self._socket.close()

    def register_ioloop(self, callback: ReplierCallback):
        """TornadoのIOLoopにメッセージ受信時のコールバックを登録.

        :param Callable callback:
        """

        def call_callback_replier(*args):
            try:
                msg = self.recv()
            except Exception as exc:
                # await callback(None, exc)
                rv = callback(None, exc)
            else:
                # await callback(msg, None)
                rv = callback(msg, None)

            if asyncio.iscoroutine(rv):
                # fire and forget
                asyncio.ensure_future(rv)

        IOLoop.current().add_handler(self, call_callback_replier, IOLoop.READ)
