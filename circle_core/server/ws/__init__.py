from circle_core.helpers import logger
from circle_core.helpers.topics import WriteDB
from circle_core.helpers.nanomsg import Sender
from tornado.websocket import WebSocketHandler


# ここからworker達にnanomsgで命令を送る
# コネクション毎にインスタンスが生成されている
class SensorHandler(WebSocketHandler):
    def open(self):
        self.__nanomsg = Sender()
        self.write_message('Greetings from Tornado!')
        logger.debug('connection opened: %s', self)

    def on_message(self, message):
        self.__nanomsg.send(WriteDB.text(message))
        logger.debug('message "%s" is sent from %s', message, self)

    def on_close(self):
        logger.debug('connection closed: %s', self)

    def check_origin(self, origin):
        # デフォルトでCORSチェックが有効になっている
        # wsta等テストツールから投げる場合はTrueにしておく
        return True
