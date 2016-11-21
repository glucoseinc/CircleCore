"""TornadoでWebSocketサーバーを立てる."""


from circle_core.helpers import logger
from circle_core.helpers.topics import WriteDB
from circle_core.helpers.nanomsg import Sender
from tornado.websocket import WebSocketHandler


class SensorHandler(WebSocketHandler):
    """ここからワーカー達にnanomsg経由で命令を送る.

    接続毎にインスタンスが生成されている

    :param Sender __nanomsg:
    """

    def open(self):
        """センサーとの接続が開いた際に呼ばれる."""
        # Senderはシングルトンだが今のところインスタンス生成の直後にsendできないので予め作っておく
        self.__nanomsg = Sender()
        self.write_message('Greetings from Tornado!')
        logger.debug('connection opened: %s', self)

    def on_message(self, message):  # TODO: messageのスキーマを決める
        """センサーからメッセージが送られてきた際に呼ばれる."""
        self.__nanomsg.send(WriteDB.text(message))
        logger.debug('message "%s" is sent from %s', message, self)

    def on_close(self):
        """センサーとの接続が切れた際に呼ばれる."""
        # TODO: 再接続？
        logger.debug('connection closed: %s', self)

    def check_origin(self, origin):
        """CORSチェック."""
        # wsta等テストツールから投げる場合はTrueにしておく
        return True
