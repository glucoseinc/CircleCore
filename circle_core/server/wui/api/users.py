# -*- coding: utf-8 -*-

"""ユーザー関連APIの実装."""

# community module
from flask import abort, redirect, request, url_for
from six import PY3

# project module
# from circle_core.cli.utils import generate_uuid
from circle_core.constants import CRScope
from circle_core.models import MessageBox, Module, User
from circle_core.server.wui.authorize.core import oauth
from .api import api, logger
from .utils import respond_failure
from ..utils import (
    api_jsonify,
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
    response = {
        'users': [user.to_json() for user in User.query]
    }
    return api_jsonify(**response)


@api.route('/users/<user_uuid>', methods=['GET', 'PUT', 'DELETE'])
def api_user(user_uuid):
    if request.method == 'GET':
        return _get_user(user_uuid)
    elif request.method == 'PUT':
        return _put_user(user_uuid)
    elif request.method == 'DELETE':
        return _delete_user(user_uuid)
    abort(405)


@oauth_require_read_users_scope
def _get_user(user_uuid):
    if user_uuid == 'me':
        # 自分の情報をゲットする
        return redirect(url_for('.api_user', user_uuid=request.oauth.user.uuid))

    user = User.query.get(user_uuid)
    if user is None:
        return respond_failure('User not found.', _status=404)

    return api_jsonify(user=user.to_json())


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


@oauth_require_read_users_scope
def _put_user(user_uuid):
    has_write, req = oauth.verify_request([CRScope.USER_RW.value])

    metadata = get_metadata()
    user = metadata.find_user(user_uuid)
    if user is None:
        return respond_failure('User not found.', _status=404)

    # TODO: viewでやるな
    # validation
    errors = {}

    if not has_write:
        # Read権限のみでは、自分の情報しか変更できない、currentPasswordが必要、permissionの変更はできない
        if str(user.uuid) != request.oauth.user:
            return respond_failure('no permission.', _status=400)

        if 'currentPassword' in request.json:
            if not user.is_password_matched(request.json['currentPassword']):
                errors['currentPassword'] = u'現在のパスワードが間違っています'
        else:
            if 'newPassword' in request.json:
                return respond_failure('user+r scope cannot change password without current.', _status=400)

        if 'permissions' in request.json:
            return respond_failure('user+r scope cannot change mine permission.', _status=400)

    if 'newPassword' in request.json:
        if not request.json['newPassword']:
            errors['newPassword'] = u'新しいパスワードが空欄です'

    if not request.json['account']:
        errors['account'] = u'アカウントは空には出来ません'

    if errors:
        return api_jsonify(_status=400, detail=dict(reason='パラメータにエラーがあります', errors=errors))

    # update
    # TODO(case変換ユーティリティ使えよ...)
    for fromName, toName in [
            ('account', 'account'), ('mailAddress', 'mail_address'), ('work', 'work'), ('telephone', 'telephone')]:
        setattr(user, toName, request.json[fromName])

    if 'permissions' in request.json:
        user.permissions = request.json['permissions']

    if 'newPassword' in request.json:
        user.set_password(request.json['newPassword'])

    metadata.unregister_user(user)
    metadata.register_user(user)
    return api_jsonify(user=user.to_json())
