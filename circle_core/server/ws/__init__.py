# -*- coding: utf-8 -*-
"""WebSocket server."""
from tornado.ioloop import IOLoop
from tornado.web import Application

from circle_core.server.ws.sensor import SensorHandler


def run(config, path, port):
    """Tornadoサーバーを立てる.

    :param str path:
    :param int part:
    """
    Application([(path, SensorHandler)], cr_config=config).listen(port)
    IOLoop.current().start()
