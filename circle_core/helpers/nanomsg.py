# -*- coding: utf-8 -*-

"""nanomsgのラッパー."""

# system module
from time import sleep
from weakref import WeakValueDictionary

# community module
from click import get_current_context
import nnpy
from six import add_metaclass, PY3
from tornado.ioloop import IOLoop

# project module
from circle_core.logger import get_stream_logger
from ..models.message import Message

if PY3:
    from json.decoder import JSONDecodeError
else:
    JSONDecodeError = ValueError

__all__ = ('Receiver', 'Sender', 'get_ipc_socket_path')
logger = get_stream_logger(__name__)


def get_ipc_socket_path():
    """Unix domain socket ファイルのパス."""
    try:
        return get_current_context().obj.ipc_socket
    except RuntimeError:
        return 'ipc:///tmp/circlecore.ipc'  # testing


class Receiver(object):
    """受信. PubSubのSub.

    :param Socket _socket:
    :param Message message:
    """

    def __init__(self, topic, message=Message):
        """接続を開く.

        :param Message message:
        """
        self._socket = nnpy.Socket(nnpy.AF_SP, nnpy.SUB)
        self._socket.connect(get_ipc_socket_path())
        logger.debug('Receiver %s', topic.topic)
        self._socket.setsockopt(nnpy.SUB, nnpy.SUB_SUBSCRIBE, topic.topic)
        self.message = message

    def __del__(self):
        """接続を閉じる."""
        self._socket.close()

    def fileno(self):
        """Tornadoに叩かれる."""
        return self._socket.getsockopt(nnpy.SOL_SOCKET, nnpy.RCVFD)

    def set_timeout(self, timeout):
        """タイムアウトを設定する.

        :param int timeout: タイムアウト millisecond
        """
        self._socket.setsockopt(nnpy.SOL_SOCKET, nnpy.RCVTIMEO, timeout)

    def incoming_messages(self):
        """メッセージを受信次第それを返すジェネレータ.

        :param TopicBase topic:
        :return Message: 受信したメッセージ
        """
        while True:
            # TODO: 接続切れたときにStopIterationしたいが自分でheartbeatを実装したりしないといけないのかな
            try:
                msg = self._socket.recv().decode('utf-8')
            except nnpy.NNError as error:
                if error.error_no == nnpy.ETIMEDOUT:
                    break
                raise

            try:
                yield self.message(msg)
            except JSONDecodeError:
                logger.warning('Received an non-JSON message. Ignore it.')

    def register_ioloop(self, callback):
        """TornadoのIOLoopにメッセージ受信時のコールバックを登録.

        :param TopicBase topic:
        """
        def call_callback(*args):
            # TODO: incoming_messagesと同じような処理が多い。共通化する
            msg = self._socket.recv().decode('utf-8')
            try:
                decoded = self.message(msg)
            except JSONDecodeError:
                logger.warning('Received an non-JSON message, Ignore it.')
            else:
                callback(decoded)

        IOLoop.current().add_handler(self, call_callback, IOLoop.READ)

    def close(self):
        """Tornadoに叩かれる."""
        IOLoop.current().remove_handler(self)


# http://stackoverflow.com/a/6798042
class Singleton(type):
    __instances = WeakValueDictionary()

    # インスタンスに()が付いたときに呼び出されるのが__call__
    # メタクラスのインスタンスはクラス
    # クラス名()で呼び出され、そのクラスのインスタンスを生成して返す
    def __call__(cls, *args, **kwargs):  # noqa
        if cls not in cls.__instances:
            logger.debug('Initialize new %s', cls.__name__)
            instance = super(Singleton, cls).__call__(*args, **kwargs)
            cls.__instances[cls] = instance
            return instance

        return cls.__instances[cls]


@add_metaclass(Singleton)
class Sender(object):
    """送信. PubSubのPub.

    同じアドレスにbindできるのは一度に一つのSocketだけなのでSingleton.

    :param Socket _socket:
    """

    def __init__(self, topic):
        """接続を開く."""
        self._socket = nnpy.Socket(nnpy.AF_SP, nnpy.PUB)
        self._socket.bind(get_ipc_socket_path())
        logger.debug('Sender %s', topic.topic)
        self.topic = topic
        sleep(0.5)  # おそらくbindが完了するまでブロックされていない。bindの直後にsendしても届かなかった。

    def __del__(self):
        """接続を閉じる."""
        self._socket.close()

    def send(self, payload):
        """送信.

        :param payload:
        """
        # nnpy.Socket.sendにunicodeを渡すとasciiでencodeしようとして例外を吐く
        self._socket.send(self.topic.encode(payload).encode('utf-8'))
