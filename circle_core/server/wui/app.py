# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
import uuid

from flask import abort, Flask, render_template, request
from six import PY3
from werkzeug.routing import BaseConverter

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

        self.url_map.converters['uuid'] = UUIDConverter

        from .api import api
        self.register_blueprint(api, url_prefix='/api')
        from .authorize import authorize, oauth
        self.register_blueprint(authorize)
        oauth.init_app(self)

        @self.route('/', defaults={'path': ''})
        @self.route('/<path:path>')
        def _index(path):
            """WUI root."""
            # ここにAPIのリクエストが来たら、それはPathを間違えている
            if request.path.startswith('/api/'):
                raise abort(404)
            return render_template('index.html')


class UUIDConverter(BaseConverter):
    """UUID値をURLに使うための今バター

    :class:`~bson.objectid.ObjectId` objects;
    :attr:`ObjectId`.
    """

    def to_python(self, value):
        try:
            return uuid.UUID(value)
        except ValueError:
            raise abort(404)

    def to_url(self, value):
        return str(value)
