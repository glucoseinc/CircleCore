# -*- coding: utf-8 -*-
"""WebSocket server."""
from six import PY3
from tornado.ioloop import IOLoop
from tornado.web import Application

from circle_core.server.ws.replication_master import ReplicationHandler
from circle_core.server.ws.sensor import SensorHandler
from ...models.metadata import MetadataIniFile, MetadataRedis

if PY3:
    from typing import Union


def run(metadata, path, port):
    """Tornadoサーバーを立てる.

    :param Union[MetadataIniFile, MetadataRedis] metadata:
    :param str path:
    :param int port:
    """
    routes = [
        (path, ReplicationHandler),
        (path + '/(?P<module_uuid>[0-9A-Fa-f-]+)', SensorHandler)
    ]
    Application(routes, cr_metadata=metadata).listen(port)
    IOLoop.current().start()
