# -*- coding: utf-8 -*-

from datetime import datetime, timedelta

from flask import Flask, render_template
from six import PY3

# project module
from circle_core.models.metadata import MetadataIniFile, MetadataRedis

if PY3:
    from typing import Optional, Union


class CCWebApp(Flask):
    def __init__(self, metadata=None):
        super(CCWebApp, self).__init__(__name__)

        self.config['METADATA'] = metadata
        self.config['TEMPLATES_AUTO_RELOAD'] = True

        from .api import api
        self.register_blueprint(api, url_prefix='/api')
        from .authorize import authorize, oauth
        self.register_blueprint(authorize)
        oauth.init_app(self)

        @self.route('/', defaults={'path': ''})
        @self.route('/<path:path>')
        def _index(path):
            """WUI root."""
            return render_template('index.html')
