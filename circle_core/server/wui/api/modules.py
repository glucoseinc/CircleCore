# -*- coding: utf-8 -*-

"""モジュール関連APIの実装."""

from .api import api
from ..utils import api_jsonify


@api.route('/modules/')
def list_modules():
    return api_jsonify(modules=[
        {'display_name': 'test', 'uuid': '0C92D140-6E74-4F6D-B2FA-4CC124DBC6DC'},
    ]
    )
