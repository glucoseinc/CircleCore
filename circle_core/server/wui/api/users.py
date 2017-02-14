# -*- coding: utf-8 -*-

"""ユーザー関連APIの実装."""

# community module
from flask import abort, request

# project module
from circle_core.constants import CRScope
from circle_core.models import MetaDataSession, User
from circle_core.server.wui.authorize.core import oauth
from .api import api
from .utils import respond_failure, respond_success
from ..utils import (
    oauth_require_read_users_scope, oauth_require_write_users_scope
)


@api.route('/users/', methods=['GET', 'POST'])
def api_users():
    if request.method == 'GET':
        return _get_users()
    # if request.method == 'POST':
    #     return _post_modules()
    abort(405)


@oauth_require_read_users_scope
def _get_users():
    return respond_success(users=[user.to_json() for user in User.query])


# @oauth_require_write_users_scope
# def _post_modules():
#     # TODO: implement
#     return respond_success()


@api.route('/users/me', methods=['GET'])
def api_user_me():
    if request.method == 'GET':
        return _get_user_me()
    abort(405)


@oauth_require_read_users_scope
def _get_user_me():
    user_uuid = request.oauth.user.uuid
    user = User.query.get(user_uuid)
    if user is None:
        return respond_failure('User not found.', _status=404)
    return respond_success(user=user.to_json())


@api.route('/users/<uuid:user_uuid>', methods=['GET', 'PUT', 'DELETE'])
def api_user(user_uuid):
    user = User.query.get(user_uuid)
    if user is None:
        return respond_failure('User not found.', _status=404)

    if request.method == 'GET':
        return _get_user(user)
    elif request.method == 'PUT':
        return _put_user(user)
    elif request.method == 'DELETE':
        return _delete_user(user)
    abort(405)


@oauth_require_read_users_scope
def _get_user(user):
    return respond_success(user=user.to_json())


@oauth_require_write_users_scope
def _delete_user(user):
    # 自分は削除できない
    if user.uuid == request.oauth.user.uuid:
        return respond_failure('Cannot delete yourself.')

    with MetaDataSession.begin():
        MetaDataSession.delete(user)

    return respond_success(user={'uuid': user.uuid})


@oauth_require_read_users_scope
def _put_user(user):
    has_write, req = oauth.verify_request([CRScope.USER_RW.value])

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
        return respond_failure('パラメータにエラーがあります', _status=400, errors=errors)

    # update
    with MetaDataSession.begin():
        user.update_from_json(request.json)

    return respond_success(user=user.to_json())
