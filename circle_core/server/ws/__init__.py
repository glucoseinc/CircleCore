# -*- coding: utf-8 -*-
"""WebSocket server."""
from tornado.ioloop import IOLoop
from tornado.web import Application

from circle_core.server.ws.sensor import SensorHandler


def run(metadata, path, port):
    """Tornadoサーバーを立てる.

    :param str path:
    :param int part:
    """
    Application([(path, SensorHandler)], cr_metadata=metadata).listen(port)
    IOLoop.current().start()
