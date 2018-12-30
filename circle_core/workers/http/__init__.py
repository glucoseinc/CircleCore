# -*- coding: utf-8 -*-
"""Master側のWebsocketの口とか、AdminのUIとか"""
import logging
import ssl
import typing

from tornado.httpserver import HTTPServer
from tornado.web import Application, FallbackHandler
from tornado.wsgi import WSGIContainer

# project module
from circle_core.exceptions import ConfigError
from circle_core.web import create_app

from .module_event import ModuleEventHandler
from .replication_master import ReplicationMasterHandler
from ..base import CircleWorker, WorkerType, register_worker_factory

logger = logging.getLogger(__name__)
WORKER_HTTP = typing.cast(WorkerType, 'http')


@register_worker_factory(WORKER_HTTP)
def create_http_worker(core, type, key, config):
    assert type == WORKER_HTTP

    def _config_get_bool(*key, **kwargs):
        return config.get(*key, **kwargs).lower() in ('on', 'true')

    return HTTPWorker(
        core,
        key,
        listen=config.get('listen'),
        ws_on=_config_get_bool('websocket'),
        ws_port=config.getint('websocket_port', fallback=config.getint('port')),
        admin_on=_config_get_bool('admin'),
        admin_port=config.getint('admin_port', fallback=config.getint('port')),
        admin_base_url=config.get('admin_base_url'),
        skip_build=_config_get_bool('skip_build'),
        tls_key_path=config.get('tls_key_path'),
        tls_crt_path=config.get('tls_crt_path')
    )


class HTTPWorker(CircleWorker):
    """
    """
    worker_type = WORKER_HTTP

    def __init__(
        self, core, worker_key, listen, ws_on, ws_port, admin_on, admin_port, admin_base_url, skip_build, tls_key_path,
        tls_crt_path
    ):
        super(HTTPWorker, self).__init__(core, worker_key)

        self.listen = listen

        self.ws_on = ws_on
        self.ws_port = ws_port

        self.admin_on = admin_on
        self.admin_port = admin_port
        self.admin_base_url = admin_base_url
        self.skip_build = skip_build
        self.flask_app = None

        if tls_key_path and not tls_crt_path:
            raise ConfigError('tls_crt_path is missing')
        elif not tls_key_path and tls_crt_path:
            raise ConfigError('tls_key_path is missing')
        self.tls_key_path = tls_key_path
        self.tls_crt_path = tls_crt_path

        if admin_on:
            if self.tls_crt_path and self.admin_base_url.startswith('http://'):
                logger.warning('admin_base_url setting (%s) startswith http, not https', self.admin_base_url)

            self.flask_app = create_app(
                self.core, self.admin_base_url, ws_port=self.ws_port, is_https=True if self.tls_crt_path else False
            )

    def initialize(self):
        if not (self.ws_on or self.admin_on):
            return

        is_https = True if self.tls_crt_path else False

        ws_handlers = []
        if self.ws_on:
            ws_handlers = [
                # モジュール用のWS
                (r'/modules/(?P<module_uuid>[0-9A-Fa-f-]+)/(?P<mbox_uuid>[0-9A-Fa-f-]+)', ModuleEventHandler),
                # Repliction用のWS
                (r'/replication/(?P<link_uuid>[0-9A-Fa-f-]+)', ReplicationMasterHandler)
            ]

        admin_handlers = []
        if self.admin_on:
            if not self.skip_build:
                self.flask_app.build_frontend()

            with self.flask_app.app_context():
                from flask import url_for
                root_url = url_for('_index', _external=True)
                assert root_url.startswith('https://' if is_https else 'http://')
                logger.info('Admin UI running on %s', root_url)

            admin_handlers = [(r'.*', FallbackHandler, {'fallback': WSGIContainer(self.flask_app)})]

        ssl_ctx = None
        if is_https:
            ssl_ctx = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
            ssl_ctx.load_cert_chain(self.tls_crt_path, self.tls_key_path)

        if self.ws_on and self.admin_on and (self.ws_port == self.admin_port):
            application = Application(
                ws_handlers + admin_handlers,  # admin_handlers must be last
                _core=self.core
            )
            server = HTTPServer(application, ssl_options=ssl_ctx)
            server.listen(self.ws_port, self.listen)
        else:
            if self.ws_on:
                ws_application = Application(ws_handlers, _core=self.core)
                ws_server = HTTPServer(ws_application, ssl_options=ssl_ctx)
                ws_server.listen(self.ws_port, self.listen)
            if self.admin_on:
                admin_application = Application(admin_handlers)
                admin_server = HTTPServer(admin_application, ssl_options=ssl_ctx)
                admin_server.listen(self.admin_port, self.listen)
