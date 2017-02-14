# -*- coding: utf-8 -*-

"""nanomsgのラッパー."""

# system module
import json
import logging
from time import sleep
from weakref import WeakValueDictionary

# community module
import nnpy
from six import add_metaclass, PY3
from tornado.ioloop import IOLoop

# project module
from .topics import TOPIC_LENGTH

if PY3:
    from json.decoder import JSONDecodeError
else:
    JSONDecodeError = ValueError

__all__ = ('Receiver', 'Sender', 'Replier',)
logger = logging.getLogger(__name__)


class Receiver(object):
    """受信. PubSubのSub.

    :param Socket _socket:
    :param BaseTopic topic:
    """

    def __init__(self, socket_url, topic=None):
        """接続を開く.

        :param BaseTopic topic:
        """
        self._socket = nnpy.Socket(nnpy.AF_SP, nnpy.SUB)
        self._socket.connect(socket_url)
        if topic:
            self._socket.setsockopt(nnpy.SUB, nnpy.SUB_SUBSCRIBE, topic.rstrip())
        self.topic = topic

    def __del__(self):
        """接続を閉じる."""
        self._socket.close()

    # def __iter__(self):
    #     """メッセージを受信次第それを返すジェネレータ.

    #     :return ModuleMessage: 受信したメッセージ
    #     """
    #     while True:
    #         # TODO: 接続切れたときにStopIterationしたいが自分でheartbeatを実装したりしないといけないのかな
    #         try:
    #             plain_msg = self._socket.recv().decode('utf-8')
    #         except nnpy.NNError as error:
    #             if error.error_no == nnpy.ETIMEDOUT:
    #                 break
    #             raise

    #         try:
    #             for msg in self.topic.decode(plain_msg):
    #                 yield msg
    #         except JSONDecodeError:
    #             logger.warning('Received an non-JSON message. Ignore it.')

    def fileno(self):
        """Tornadoに叩かれる."""
        return self._socket.getsockopt(nnpy.SOL_SOCKET, nnpy.RCVFD)

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
        def call_callback(*args):
            # TODO: topicを設定している場合、違うTopicのパケットがきてもpollが反応するのでdontwaitにしてチェックしないといけないかも
            try:
                raw = self._socket.recv()
                plain_msg = raw.decode('utf-8')
                topic, message = plain_msg[:TOPIC_LENGTH], plain_msg[TOPIC_LENGTH:]
                message = json.loads(message)
                callback(topic, message)
            except:
                import traceback
                traceback.print_exc()

        IOLoop.current().add_handler(self, call_callback, IOLoop.READ)


# # http://stackoverflow.com/a/6798042
# class Singleton(type):
#     __instances = WeakValueDictionary()

#     # インスタンスに()が付いたときに呼び出されるのが__call__
#     # メタクラスのインスタンスはクラス
#     # クラス名()で呼び出され、そのクラスのインスタンスを生成して返す
#     def __call__(cls, *args, **kwargs):  # noqa
#         if cls not in cls.__instances:
#             logger.debug('Initialize new %s', cls.__name__)
#             instance = super(Singleton, cls).__call__(*args, **kwargs)
#             cls.__instances[cls] = instance
#             return instance

#         logger.debug('Reuse existing %s', cls.__name__)
#         return cls.__instances[cls]


# @add_metaclass(Singleton)
class Sender(object):
    """送信. PubSubのPub.

    同じアドレスにbindできるのは一度に一つのSocketだけなのでSingleton.

    :param Socket _socket:
    """

    def __init__(self, socket_url):
        """接続を開く."""
        self._socket = nnpy.Socket(nnpy.AF_SP, nnpy.PUB)
        self._socket.bind(socket_url)
        # # TODO: bindの名前解決がasyncで行われるはずなので、それをスマートに待機する方法を調べておく
        # sleep(0.5)  # おそらくbindが完了するまでブロックされていない。bindの直後にsendしても届かなかった。

    def __del__(self):
        """接続を閉じる."""
        self._socket.close()

    def send(self, topic, payload):
        """送信.

        :param payload:
        """
        # nnpy.Socket.sendにunicodeを渡すとasciiでencodeしようとして例外を吐く
        # self._socket.send(self.topic.encode(payload).encode('utf-8'))
        data = topic.ljust(48) + json.dumps(payload)
        return self._socket.send(data.encode('utf-8'))


class Replier(object):
    def __init__(self, socket_url):
        """接続を開く."""
        self._socket = nnpy.Socket(nnpy.AF_SP, nnpy.REP)
        self._socket.bind(socket_url)
        # # TODO: bindの名前解決がasyncで行われるはずなので、それをスマートに待機する方法を調べておく
        # sleep(0.5)  # おそらくbindが完了するまでブロックされていない。bindの直後にsendしても届かなかった。

    def __del__(self):
        """接続を閉じる."""
        self._socket.close()

    def recv(self):
        """受信
        """
        raw = self._socket.recv()
        return json.loads(raw.decode('utf-8'))

    def send(self, payload):
        """送信.

        :param payload:
        """
        data = json.dumps(payload)
        return self._socket.send(data.encode('utf-8'))

    def fileno(self):
        """Tornadoに叩かれる."""
        return self._socket.getsockopt(nnpy.SOL_SOCKET, nnpy.RCVFD)

    def close(self):
        """Tornadoに叩かれる."""
        self._socket.close()

    def register_ioloop(self, callback):
        """TornadoのIOLoopにメッセージ受信時のコールバックを登録.

        :param FunctionType callback:
        """
        def call_callback(*args):
            try:
                msg = self.recv()
            except Exception as exc:
                callback(None, exc)
            else:
                callback(msg, None)

        IOLoop.current().add_handler(self, call_callback, IOLoop.READ)
