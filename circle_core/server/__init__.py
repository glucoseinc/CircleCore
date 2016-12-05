# -*- coding: utf-8 -*-
"""WebSocketはTornado, HTTPはFlaskで捌く."""
from tornado.ioloop import IOLoop
from tornado.web import Application, FallbackHandler
from tornado.wsgi import WSGIContainer

from circle_core.server.ws.sensor import SensorHandler
from circle_core.server.wui import create_app


def run(port=5000, metadata=None):
    """TornadoサーバーとFlaskサーバーを立てる.

    clickから起動される.
    """
    # meinheldとか使う場合はこのファイルに追記していくことになるのかな
    print('start combined server')
    flask_app = create_app(metadata)
    tornado_app = Application([
        (r'/ws/(?P<device_uuid>[0-9A-Fa-f-]+)', SensorHandler),
        (r'.*', FallbackHandler, {'fallback': WSGIContainer(flask_app)})
    ],
        cr_metadata=metadata
    )
    # パフォーマンスの問題があるので別々のサーバーとして立てることも可能にする
    # http://www.tornadoweb.org/en/stable/wsgi.html#tornado.wsgi.WSGIContainer

    tornado_app.listen(port)
    IOLoop.current().start()
