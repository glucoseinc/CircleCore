from tornado.websocket import WebSocketHandler


# ここからworker達にnanomsgで命令を送る？
# コネクション毎にインスタンスが生成されている
class SensorHandler(WebSocketHandler):
  # 普通に走らせた場合はこのクラス属性に全てのコネクションが入るんだろうが
  # gunicorn等の上で動かした場合も大丈夫なのかな　よくわかってない
  waiters = set()

  def open(self):
    print('open:', self)  # TODO: Use logging
    SensorHandler.waiters.add(self)
    self.write_message('Greetings from Tornado!')

  def on_message(self, message):
    print('message "{}" is sent to {}'.format(message, self))
    for connection in SensorHandler.waiters:
      connection.write_message(message)

  def on_close(self):
    print('close:', self)
    SensorHandler.waiters.remove(self)

  def check_origin(self, origin):
    # デフォルトでCORSチェックが有効になっている
    # wsta等テストツールから投げる場合はTrueにしておく
    return True
