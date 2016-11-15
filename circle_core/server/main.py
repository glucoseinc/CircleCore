from tornado.wsgi import WSGIContainer, WSGIAdapter
from tornado.web import Application, FallbackHandler
from tornado.ioloop import IOLoop
from wui import create_app
from ws import SensorHandler


# meinheldとか使う場合はこのファイルに追記していくことになるのかな
flask_app = create_app()
tornado_app = Application([
  (r'/ws/?', SensorHandler),
  (r'.*', FallbackHandler, {'fallback': WSGIContainer(flask_app)})
])
# FIXME: See warning http://www.tornadoweb.org/en/stable/wsgi.html#tornado.wsgi.WSGIContainer
# これだとパフォーマンスに悪影響が出るっぽいのでどうしようか


if __name__ == '__main__':
  tornado_app.listen(5000)
  IOLoop.current().start()
