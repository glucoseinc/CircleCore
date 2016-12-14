# -*- coding: utf-8 -*-
"""WebUI."""

# community module
from flask import Flask, render_template
from six import PY3

# project module
from ...models.metadata import MetadataIniFile, MetadataRedis

if PY3:
    from typing import Optional, Union


app = Flask(__name__)
app.metadata = None  # type: Optional[Union[MetadataIniFile, MetadataRedis]]


@app.route('/')
def index():
    """仮."""
    return 'Greetings from flask!'


@app.route('/schema/list')
def schema_list():
    """スキーマリスト."""
    context = {}

    metadata = app.metadata
    if metadata is not None:
        context['schemas'] = metadata.schemas
    return render_template('schema_list.html', **context)


def create_app(metadata=None):
    """App factory."""
    # TODO: Use blueprint
    app.metadata = metadata
    return app
