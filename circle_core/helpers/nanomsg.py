# -*- coding: utf-8 -*-

"""nanomsgのラッパー."""

# system module
from time import sleep

# community module
from click import get_current_context
import nnpy
from six import add_metaclass, PY3
from tornado.ioloop import IOLoop

# project module
from circle_core.logger import get_stream_logger

if PY3:
    from json.decoder import JSONDecodeError
else:
    JSONDecodeError = ValueError

__all__ = ('Receiver', 'Sender', 'get_ipc_socket_path')
logger = get_stream_logger(__name__)


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
        self.__socket = nnpy.Socket(nnpy.AF_SP, nnpy.SUB)
        self.__socket.connect(get_ipc_socket_path())

    def __del__(self):
        """接続を閉じる."""
        self.__socket.close()

    def set_timeout(self, timeout):
        """タイムアウトを設定する

        :param int timeout: タイムアウト millisecond
        """
        self.__socket.setsockopt(nnpy.SOL_SOCKET, nnpy.RCVTIMEO, timeout)

    def incoming_messages(self, topic):
        """メッセージを受信次第それを返すジェネレータ.

        :param TopicBase topic:
        :return unicode: 受信したメッセージ
        """
        self.__socket.setsockopt(nnpy.SUB, nnpy.SUB_SUBSCRIBE, topic.topic)
        while True:
            # TODO: 接続切れたときにStopIterationしたいが自分でheartbeatを実装したりしないといけないのかな
            try:
                msg = self.__socket.recv().decode('utf-8')
            except nnpy.NNError as error:
                if error.error_no == nnpy.ETIMEDOUT:
                    break
                raise

            try:
                yield topic.decode_json(msg)
            except JSONDecodeError:
                logger.warning('Received an non-JSON message. Ignore it.')

    def register_ioloop(self, topic, callback):
        """TornadoのIOLoopにメッセージ受信時のコールバックを登録.

        :param TopicBase topic:
        """

        def call_callback(*args):
            # TODO: incoming_messagesと同じような処理が多い。共通化する
            msg = self.__socket.recv().decode('utf-8')
            try:
                decoded = topic.decode_json(msg)
            except JSONDecodeError:
                logger.warning('Received an non-JSON message, Ignore it.')
            else:
                callback(decoded)

        self.__socket.setsockopt(nnpy.SUB, nnpy.SUB_SUBSCRIBE, topic.topic)
        fileno = self.__socket.getsockopt(nnpy.SOL_SOCKET, nnpy.RCVFD)
        IOLoop.current().add_handler(fileno, call_callback, IOLoop.READ)


# http://stackoverflow.com/a/6798042
class Singleton(type):
    __instances = {}

    # インスタンスに()が付いたときに呼び出されるのが__call__
    # メタクラスのインスタンスはクラス
    # クラス名()で呼び出され、そのクラスのインスタンスを生成して返す
    def __call__(cls, *args, **kwargs):  # noqa
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
        self.__socket = nnpy.Socket(nnpy.AF_SP, nnpy.PUB)
        self.__socket.bind(get_ipc_socket_path())
        # 同じアドレスにbindできるのは一度に一つのSocketだけ
        sleep(0.5)
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
