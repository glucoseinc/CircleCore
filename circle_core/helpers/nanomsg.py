#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""nanomsgのラッパー."""
from time import sleep
from logging import getLogger

from click import get_current_context
from nnpy import AF_SP, PUB, Socket, SUB, SUB_SUBSCRIBE
from six import add_metaclass, PY3

from circle_core.helpers.topics import TOPIC_LENGTH

if PY3:
    from json.decoder import JSONDecodeError
else:
    JSONDecodeError = ValueError

__all__ = ('Receiver', 'Sender', 'get_ipc_socket_path')
logger = getLogger(__name__)


def get_ipc_socket_path():
    try:
        return get_current_context().obj.ipc_socket
    except RuntimeError:
        return 'ipc:///tmp/circlecore.ipc'  # testing


class Receiver(object):
    """受信. PubSubのSub.

    :param Socket __socket:
    """

    def __init__(self):
        """接続を開く."""
        self.__socket = Socket(AF_SP, SUB)
        self.__socket.connect(get_ipc_socket_path())

    def __del__(self):
        """接続を閉じる."""
        self.__socket.close()

    def incoming_messages(self, topic):
        """メッセージを受信次第それを返すジェネレータ.

        :param TopicBase topic:
        :return unicode: 受信したメッセージ
        """
        self.__socket.setsockopt(SUB, SUB_SUBSCRIBE, topic.justify())
        while True:
            # TODO: 接続切れたときにStopIterationしたいが自分でheartbeatを実装したりしないといけないのかな
            msg = self.__socket.recv().decode('utf-8')
            try:
                yield topic.decode_json(msg)
            except JSONDecodeError:
                logger.warning('Received an non-JSON message. Ignore it.')


# http://stackoverflow.com/a/6798042
class Singleton(type):
    __instances = {}

    # インスタンスに()が付いたときに呼び出されるのが__call__
    # メタクラスのインスタンスはクラス
    # クラス名()で呼び出され、そのクラスのインスタンスを生成して返す
    def __call__(cls, *args, **kwargs):
        if cls not in cls.__instances:
            cls.__instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls.__instances[cls]


@add_metaclass(Singleton)
class Sender(object):
    """送信. PubSubのPub.

    :param Socket __socket:
    """

    def __init__(self):
        """接続を開く."""
        self.__socket = Socket(AF_SP, PUB)
        self.__socket.bind(get_ipc_socket_path())
        # 同じアドレスにbindできるのは一度に一つのSocketだけ
        sleep(0.1)
        # おそらくbindが完了するまでブロックされていない
        # bindの直後にsendしても届かなかった

    def __del__(self):
        """接続を閉じる."""
        self.__socket.close()

    def send(self, msg):
        """送信.

        :param unicode msg:
        """
        # nnpy.Socket.sendにunicodeを渡すとasciiでencodeしようとして例外を吐く
        self.__socket.send(msg.encode('utf-8'))
