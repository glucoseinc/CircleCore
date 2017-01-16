# -*- coding: utf-8 -*-
"""WebSocket server."""
from six import PY3
from tornado.ioloop import IOLoop
from tornado.web import Application

from circle_core.server.ws.module import ModuleHandler
from circle_core.server.ws.replication_master import ReplicationMaster
from ...models.metadata import MetadataIniFile, MetadataRedis

if PY3:
    from typing import Union


def run(metadata, path, port):
    """Tornadoサーバーを立てる.

    :param Union[MetadataIniFile, MetadataRedis] metadata:
    :param str path:
    :param int port:
    """
    Application([
        (path, ReplicationMaster),
        (path + '/(?P<module_uuid>[0-9A-Fa-f-]+)', ModuleHandler)
    ]).listen(port)
    IOLoop.current().start()
