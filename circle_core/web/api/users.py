# -*- coding: utf-8 -*-
"""ユーザー関連APIの実装."""

# community module
from flask import abort, request

# project module
from circle_core.constants import CRScope
from circle_core.models import MetaDataSession, User

from .api import api
from .utils import respond_failure, respond_success
from ..authorize.core import oauth
from ..utils import oauth_require_read_users_scope, oauth_require_write_users_scope


@api.route('/users/', methods=['GET', 'POST'])
def api_users():
    """全てのUserのCRUD."""
    if request.method == 'GET':
        return _get_users()
    # if request.method == 'POST':
    #     return _post_modules()
    abort(405)


@oauth_require_read_users_scope
def _get_users():
    """全てのUserの情報を取得する.

    :return: 全てのUserの情報
    :rtype: Response
    """
    return respond_success(users=[user.to_json(
        request.oauth.user.is_admin() or user.uuid == request.oauth.user.uuid
    ) for user in User.query])


@api.route('/users/me', methods=['GET'])
def api_user_me():
    """自身のUserのCRUD."""
    if request.method == 'GET':
        return _get_user_me()
    abort(405)


@oauth_require_read_users_scope
def _get_user_me():
    """自身のUserの情報を取得する.

    :return: 自身のUserの情報
    :rtype: Response
    """
    user_uuid = request.oauth.user.uuid
    user = User.query.get(user_uuid)
    if user is None:
        return respond_failure('User not found.', _status=404)
    return respond_success(user=user.to_json(True))


@api.route('/users/<uuid:user_uuid>', methods=['GET', 'PUT', 'DELETE'])
def api_user(user_uuid):
    """単一のUserのCRUD."""
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


@api.route('/users/<uuid:user_uuid>/renewToken', methods=['POST'])
@oauth_require_read_users_scope
def api_user_renew_token(user_uuid):
    """UserのTokenを再生する

    admin ... 全員
    user ... 自分だけ
    """
    user = User.query.get(user_uuid)
    if user is None:
        return respond_failure('User not found.', _status=404)

    if not request.oauth.user.is_admin():
        if user.uuid != request.oauth.user.uuid:
            return respond_failure('Permission denied.')

    with MetaDataSession.begin():
        user.renew_token()

    return respond_success(user=user.to_json(True))


@oauth_require_read_users_scope
def _get_user(user):
    """Userの情報を取得する.

    :param User user: 取得するUser
    :return: Userの情報
    :rtype: Response
    """
    respond_full = request.oauth.user.is_admin() or user.uuid == request.oauth.user.uuid
    return respond_success(user=user.to_json(respond_full))


@oauth_require_read_users_scope
def _put_user(user):
    """Userを更新する.

    :param User user: 更新するUser
    :return: Userの情報
    :rtype: Response
    """
    has_write, req = oauth.verify_request([CRScope.USER_RW.value])

    # TODO: viewでやるな
    # validation
    errors = {}

    if not has_write:
        # Read権限のみでは、自分の情報しか変更できない、currentPasswordが必要、permissionの変更はできない
        if user.uuid != request.oauth.user.uuid:
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
        if len(request.json['newPassword']) < 6:
            errors['newPassword'] = u'パスワードは6文字以上にしてください'

    if not request.json['account']:
        errors['account'] = u'アカウントは空には出来ません'

    if errors:
        return respond_failure('パラメータにエラーがあります', _status=400, errors=errors)

    # update
    with MetaDataSession.begin():
        user.update_from_json(request.json)

    respond_full = request.oauth.user.is_admin() or user.uuid == request.oauth.user.uuid
    return respond_success(user=user.to_json(respond_full))


@oauth_require_write_users_scope
def _delete_user(user):
    """Userを削除する.

    :param User user: 削除するUser
    :return: Userの情報
    :rtype: Response
    """
    # 自分は削除できない
    if user.uuid == request.oauth.user.uuid:
        return respond_failure('Cannot delete yourself.')

    with MetaDataSession.begin():
        MetaDataSession.delete(user)

    return respond_success(user={'uuid': user.uuid})
