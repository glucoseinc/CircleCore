# -*- coding: utf-8 -*-
"""Master側のWebsocketの口とか、AdminのUIとか"""
import logging
import ssl

from tornado.httpserver import HTTPServer
from tornado.web import Application, FallbackHandler
from tornado.wsgi import WSGIContainer

# project module
from circle_core.constants import RequestType
from circle_core.exceptions import ConfigError
from circle_core.server.wui import create_app
from .replication_master import ReplicationMaster
from ..base import CircleWorker, register_worker_factory

logger = logging.getLogger(__name__)
WORKER_HTTP = 'http'


@register_worker_factory(WORKER_HTTP)
def create_http_worker(core, type, key, config):
    assert type == WORKER_HTTP

    def _config_get_bool(*key, **kwargs):
        return config.get(*key, **kwargs).lower() in ('on', 'true')

    return HTTPWorker(
        core, key,
        listen=config.get('listen'),
        port=config.getint('port'),
        websocket_on=_config_get_bool('websocket'),
        admin_on=_config_get_bool('admin'),
        admin_base_url=config.get('admin_base_url', fallback='http://${listen}:${port}'),
        skip_build=_config_get_bool('skip_build'),
        tls_key_path=config.get('tls_key_path'),
        tls_crt_path=config.get('tls_crt_path')
    )


class HTTPWorker(CircleWorker):
    """
    """
    worker_type = WORKER_HTTP

    def __init__(self, core, worker_key, listen, port, websocket_on, admin_on, admin_base_url, skip_build,
                 tls_key_path, tls_crt_path):
        super(HTTPWorker, self).__init__(core, worker_key)

        self.port = port
        self.listen = listen
        self.websocket_on = websocket_on
        self.admin_on = admin_on

        if tls_key_path and tls_crt_path:
            self.tls_key_path = tls_key_path
            self.tls_crt_path = tls_crt_path
        elif tls_key_path:
            raise ConfigError('tls_crt_path is missing')
        elif tls_crt_path:
            raise ConfigError('tls_key_path is missing')
        else:
            self.tls_key_path = None
            self.tls_crt_path = None

        self.request_handlers = []

        if self.websocket_on:
            self.request_handlers.append(
                (r'/replication/(?P<link_uuid>[0-9A-Fa-f-]+)', ReplicationMaster),
            )

        self.flask_app = None
        if self.admin_on:
            # must be last
            self.flask_app = create_app(core, admin_base_url)
            self.request_handlers.append(
                (r'.*', FallbackHandler, {'fallback': WSGIContainer(self.flask_app)})
            )

        kwargs = {'_core': core}
        self.application = Application(self.request_handlers, **kwargs)
        self.skip_build = skip_build

    def initialize(self):
        if self.flask_app and not self.skip_build:
            self.flask_app.build_frontend()

        if self.flask_app:
            with self.flask_app.test_request_context('/'):
                from flask import url_for
                logger.info('Admin UI running on %s', url_for('_index', _external=True))

        if self.request_handlers:
            if self.tls_crt_path:
                ssl_ctx = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
                ssl_ctx.load_cert_chain(self.tls_crt_path, self.tls_key_path)
                server = HTTPServer(self.application, ssl_options=ssl_ctx)
                server.listen(self.port, self.listen)
            else:
                self.application.listen(self.port, self.listen)
