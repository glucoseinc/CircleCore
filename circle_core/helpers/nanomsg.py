#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""nanomsgのラッパー."""
from nnpy import AF_SP, PUB, Socket, SUB, SUB_SUBSCRIBE
from six import add_metaclass
__all__ = ('Receiver', 'Sender')


class Receiver:
    """受信. PubSubのSub.

    :param Socket __socket:
    """

    def __init__(self):
        """接続を開く."""
        self.__socket = Socket(AF_SP, SUB)
        self.__socket.connect('ipc:///tmp/hoge.ipc')

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
            # TODO: 接続切れたときの対応
            yield self.__socket.recv()


# http://stackoverflow.com/a/6798042
class Singleton(type):
    __instances = {}

    # インスタンスに()が付いたときに呼び出されるのが__call__
    # メタクラスのインスタンスはクラス
    # クラス名()で呼び出され、そのクラスのインスタンスを生成して返す
    def __call__(cls, *args, **kwargs):
        if cls not in cls.__instances:
            cls.__instances[cls] = super().__call__(*args, **kwargs)
        return cls.__instances[cls]


@add_metaclass(Singleton)
class Sender:
    """送信. PubSubのPub.

    :param Socket __socket:
    """

    def __init__(self):
        """接続を開く."""
        self.__socket = Socket(AF_SP, PUB)
        self.__socket.bind('ipc:///tmp/hoge.ipc')
        # 同じアドレスにbindできるのは一度に一つのSocketだけ
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
