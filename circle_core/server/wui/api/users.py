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


@api.route('/users/<user_uuid>', methods=['PUT', 'DELETE'])
def api_user(user_uuid):
    if request.method == 'PUT':
        return _put_user(user_uuid)
    if request.method == 'DELETE':
        return _delete_user(user_uuid)
    abort(405)


@oauth_require_write_users_scope
def _delete_user(user_uuid):
    # 自分は削除できない
    metadata = get_metadata()
    user = metadata.find_user(user_uuid)
    if user is None:
        return respond_failure('User not found.', _status=404)

    if str(user.uuid) == request.oauth.user:
        return respond_failure('Cannot delete yourself.')

    metadata.unregister_user(user)
    return api_jsonify(user={'uuid': user.uuid})


@oauth_require_write_users_scope
def _put_user(user_uuid):
    metadata = get_metadata()
    user = metadata.find_user(user_uuid)
    if user is None:
        return respond_failure('User not found.', _status=404)

    # TODO: viewでやるな
    # validation
    errors = {}

    if 'currentPassword' in request.json:
        if not user.is_password_matched(request.json['currentPassword']):
            errors['currentPassword'] = u'現在のパスワードが間違っています'
        if not request.json['newPassword']:
            errors['newPassword'] = u'新しいパスワードが空欄です'

    if not request.json['account']:
        errors['account'] = u'アカウントは空には出来ません'
    if errors:
        return api_jsonify(_status=400, detail=dict(reason='パラメータにエラーがあります', errors=errors))

    # update
    # TODO(case変換ユーティリティ使えよ...)
    for fromName, toName in [
            ('account', 'account'), ('mailAddress', 'mail_address'), ('work', 'work'), ('telephone', 'telephone'),
            ('permissions', 'permissions')]:
        setattr(user, toName, request.json[fromName])

    if 'newPassword' in request.json:
        user.set_password(request.json['newPassword'])

    metadata.unregister_user(user)
    metadata.register_user(user)
    return api_jsonify(user=user.to_json())
