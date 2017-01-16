# -*- coding: utf-8 -*-

"""ユーザー関連APIの実装."""

# community module
from flask import abort, request
from six import PY3

# project module
from circle_core.cli.utils import generate_uuid
from circle_core.models import MessageBox, Module
from .api import api
from .utils import respond_failure
from ..utils import (
    api_jsonify, convert_dict_key_camel_case, convert_dict_key_snake_case, get_metadata,
    oauth_require_read_users_scope, oauth_require_write_users_scope
)

if PY3:
    from typing import Any, Dict


@api.route('/users/', methods=['GET', 'POST'])
def api_users():
    if request.method == 'GET':
        return _get_users()
    # if request.method == 'POST':
    #     return _post_modules()
    abort(405)


@oauth_require_read_users_scope
def _get_users():
    users = get_metadata().users

    response = {
        'users': [user.to_json() for user in users]
    }
    return api_jsonify(**response)


@api.route('/users/<user_uuid>', methods=['GET', 'DELETE'])
def api_user(user_uuid):
    # if request.method == 'GET':
    #     return _get_module(module_uuid)
    # if request.method == 'PUT':
    #     return _put_module(module_uuid)
    if request.method == 'DELETE':
        return _delete_user(user_uuid)
    abort(405)


@oauth_require_write_users_scope
def _delete_user(user_uuid):
    # 自分は削除できない
    metadata = get_metadata()
    user = metadata.find_user(user_uuid)
    if user is None:
        return respond_failure('User not found.')

    if str(user.uuid) == request.oauth.user:
        return respond_failure('Cannot delete yourself.')

    metadata.unregister_user(user)
    return api_jsonify(user={'uuid': user.uuid})
