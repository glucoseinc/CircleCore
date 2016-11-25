#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""nanomsgのラッパー."""
from time import sleep

from circle_core.helpers.topics import TOPIC_LENGTH
from nnpy import AF_SP, PUB, Socket, SUB, SUB_SUBSCRIBE
from six import add_metaclass
__all__ = ('Receiver', 'Sender')


SOCKET_PATH = 'ipc:///tmp/hoge.ipc'  # TODO: CLIから指定


class Receiver:
    """受信. PubSubのSub.

    :param Socket __socket:
    """

    def __init__(self, socket_path=SOCKET_PATH):
        """接続を開く."""
        self.__socket = Socket(AF_SP, SUB)
        self.__socket.connect(socket_path)

    def __del__(self):
        """接続を閉じる."""
        self.__socket.close()

    def incoming_messages(self, topic):
        """メッセージを受信次第それを返すジェネレータ.

        :param TopicBase topic:
        :return: 受信したメッセージ
        """
        self.__socket.setsockopt(SUB, SUB_SUBSCRIBE, topic.justify())
        while True:
            # TODO: 接続切れたときにStopIterationしたいが自分でheartbeatを実装したりしないといけないのかな
            msg = self.__socket.recv()
            yield msg.decode('utf-8')[TOPIC_LENGTH:]


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
class Sender:
    """送信. PubSubのPub.

    :param Socket __socket:
    """

    def __init__(self, socket_path=SOCKET_PATH):
        """接続を開く.

        :param str socket_path: ipc://で始まる
        """
        self.__socket = Socket(AF_SP, PUB)
        self.__socket.bind(socket_path)
        # 同じアドレスにbindできるのは一度に一つのSocketだけ
        sleep(0.1)
        # おそらくbindが完了するまでブロックされていない
        # bindの直後にsendしても届かなかった

    def __del__(self):
        """接続を閉じる."""
        self.__socket.close()

    def send(self, msg):
        """送信.

        :param str msg:
        """
        self.__socket.send(msg)
