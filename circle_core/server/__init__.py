#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""WebSocketはTornado, HTTPはFlaskで捌く."""
from tornado.wsgi import WSGIContainer
from tornado.web import Application, FallbackHandler
from tornado.ioloop import IOLoop
from circle_core.server.wui import create_app
from circle_core.server.ws import SensorHandler


# meinheldとか使う場合はこのファイルに追記していくことになるのかな
flask_app = create_app()
tornado_app = Application([
    (r'/ws/?', SensorHandler),
    (r'.*', FallbackHandler, {'fallback': WSGIContainer(flask_app)})
])
# FIXME: See warning http://www.tornadoweb.org/en/stable/wsgi.html#tornado.wsgi.WSGIContainer
# これだとパフォーマンスに悪影響が出るっぽいのでどうしようか


def run():
    """TornadoサーバーとFlaskサーバーを立てる.

    clickから起動される.
    """
    tornado_app.listen(5000)
    IOLoop.current().start()
