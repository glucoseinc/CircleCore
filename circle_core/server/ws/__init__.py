from circle_core.utils import logger
from circle_core.topics import WriteDB
from tornado.websocket import WebSocketHandler
from nnpy import Socket, PUB, AF_SP


# ここからworker達にnanomsgで命令を送る？
# コネクション毎にインスタンスが生成されている
class SensorHandler(WebSocketHandler):
    socket = None

    def open(self):
        if self.socket is None:
            # TODO: NanomsgSenderとか作る
            self.socket = Socket(AF_SP, PUB)
            self.socket.bind('ipc:///tmp/hoge.ipc')

        self.write_message('Greetings from Tornado!')
        logger.debug('connection opened: %s', self)

    def on_message(self, message):
        global socket
        self.socket.send(WriteDB.text(message))
        logger.debug('message "%s" is sent from %s', message, self)

    def on_close(self):
        logger.debug('connection closed: %s', self)

    def check_origin(self, origin):
        # デフォルトでCORSチェックが有効になっている
        # wsta等テストツールから投げる場合はTrueにしておく
        return True
