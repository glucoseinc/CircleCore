#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""WebUI."""

# community module
from flask import Flask, render_template
from six import PY3

# project module
from ...models import Config

if PY3:
    from typing import Optional


app = Flask(__name__)
app.my_config = None  # type: Optional[Config]


@app.route('/')
def index():
    """仮."""
    return 'Greetings from flask!'


@app.route('/schema/list')
def schema_list():
    """スキーマリスト."""
    context  = {}

    config = app.my_config
    if config is not None:
        config.instantiate_all_schemas()
        context['schemas'] = config.schemas
    return render_template('schema_list.html', **context)


def create_app(config=None):
    """App factory."""
    # TODO: Use blueprint
    app.my_config = config
    return app
