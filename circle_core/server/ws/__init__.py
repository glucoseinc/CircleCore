from circle_core.utils import logger
from tornado.websocket import WebSocketHandler


# ここからworker達にnanomsgで命令を送る？
# コネクション毎にインスタンスが生成されている
class SensorHandler(WebSocketHandler):
    # 普通に走らせた場合はこのクラス属性に全てのコネクションが入るんだろうが
    # gunicorn等の上で動かした場合も大丈夫なのかな　よくわかってない
    waiters = set()

    def open(self):
        SensorHandler.waiters.add(self)
        self.write_message('Greetings from Tornado!')
        logger.debug('connection opened: %s', self)

    def on_message(self, message):
        for connection in SensorHandler.waiters:
            connection.write_message(message)
            logger.debug('message "%s" is sent from %s', message, self)

    def on_close(self):
        SensorHandler.waiters.remove(self)
        logger.debug('connection closed: %s', self)

    def check_origin(self, origin):
        # デフォルトでCORSチェックが有効になっている
        # wsta等テストツールから投げる場合はTrueにしておく
        return True
