# -*- coding: utf-8 -*-
"""Master側のWebsocketの口とか、AdminのUIとか"""

import logging

from tornado.web import Application, FallbackHandler
from tornado.wsgi import WSGIContainer

# project module
from circle_core.constants import RequestType
from circle_core.server.wui import create_app
from .base import CircleWorker, register_worker_factory


logger = logging.getLogger(__name__)
WORKER_HTTP = 'http'


@register_worker_factory(WORKER_HTTP)
def create_http_worker(core, type, key, config):
    assert type == WORKER_HTTP

    def _config_get_bool(*key, **kwargs):
        return config.get(*key, **kwargs).lower() in ('on', 'true')

    return HTTPWorker(
        core,
        listen=config.get('listen'),
        port=config.getint('port'),
        websocket_on=_config_get_bool('websocket'),
        admin_on=_config_get_bool('admin'),
        admin_base_url=config.get('admin_base_url', fallback='http://${listen}:${port}'),
        skip_build=_config_get_bool('skip_build')
    )


class HTTPWorker(CircleWorker):
    """
    """

    def __init__(self, core, listen, port, websocket_on, admin_on, admin_base_url, skip_build):
        super(HTTPWorker, self).__init__(core)

        self.port = port
        self.listen = listen
        self.websocket_on = websocket_on
        self.admin_on = admin_on

        self.request_handlers = []

        if self.websocket_on:
            pass

        self.flask_app = None
        if self.admin_on:
            # must be last
            self.flask_app = create_app(core, admin_base_url)
            self.request_handlers.append(
                (r'.*', FallbackHandler, {'fallback': WSGIContainer(self.flask_app)})
            )

        kwargs = {}
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
            self.application.listen(self.port, self.listen)
