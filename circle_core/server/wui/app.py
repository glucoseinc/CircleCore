# -*- coding: utf-8 -*-

from datetime import datetime, timedelta

from flask import Flask, render_template
from six import PY3

# project module
from circle_core.models.metadata import MetadataIniFile, MetadataRedis

if PY3:
    from typing import Optional, Union


class CCWebApp(Flask):
    """Web管理インタフェース用のFlask Application
    """
    def __init__(self, metadata=None):
        super(CCWebApp, self).__init__(__name__)

        self.config['SECRET_KEY'] = (
            '16f4ecd3a212450c3bbc22f61c2fa4ea06c5ae7fa8827887e14b469ab59d69d6'
            '574302c7680310a50a5dc70db38d584ace529f0162ec56103cbce6a4c670e417'
        )
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
