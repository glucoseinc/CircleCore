#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""WebSocketはTornado, HTTPはFlaskで捌く."""
from tornado.ioloop import IOLoop
from tornado.web import Application, FallbackHandler
from tornado.wsgi import WSGIContainer

from circle_core.server.ws.sensor import SensorHandler
from circle_core.server.wui import create_app


def run(port=5000, config=None):
    """TornadoサーバーとFlaskサーバーを立てる.

    clickから起動される.
    """
    # meinheldとか使う場合はこのファイルに追記していくことになるのかな
    flask_app = create_app(config)
    tornado_app = Application([
        (r'/ws/?', SensorHandler),
        (r'.*', FallbackHandler, {'fallback': WSGIContainer(flask_app)})
    ])
    # パフォーマンスの問題があるので別々のサーバーとして立てることも可能にする
    # http://www.tornadoweb.org/en/stable/wsgi.html#tornado.wsgi.WSGIContainer

    tornado_app.listen(port)
    IOLoop.current().start()
