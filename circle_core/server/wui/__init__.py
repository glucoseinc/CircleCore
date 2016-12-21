# -*- coding: utf-8 -*-

"""WebUI."""

# community module
from flask import Flask, render_template
from six import PY3

# project module
from circle_core.models.metadata import MetadataIniFile, MetadataRedis
from .api import api

if PY3:
    from typing import Optional, Union


def _index():
    """WUI root."""
    return render_template('index.html')


def create_app(metadata=None):
    """App factory.

    :param Optional[Union[MetadataIniFile, MetadataRedis]] metadata: Metadata
    :rtype: Flask
    """
    app = Flask(__name__)
    app.register_blueprint(api)
    app.config['METADATA'] = metadata
    app.config['TEMPLATES_AUTO_RELOAD'] = True

    app.add_url_rule('/', 'index', _index)

    return app
