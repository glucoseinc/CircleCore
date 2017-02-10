# -*- coding: utf-8 -*-
"""WebSocket server."""
from six import PY3
from tornado.ioloop import IOLoop
from tornado.web import Application

from circle_core.server.ws.replication_master import ReplicationMaster

if PY3:
    from typing import Union


def run(path, port, debug):
    """Tornadoサーバーを立てる.

    :param str path:
    :param int port:
    """
    Application([
        (path, ReplicationMaster),
    ], debug=debug).listen(port)
    IOLoop.current().start()
