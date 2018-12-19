# -*- coding: utf-8 -*-
"""Flask download Blueprint."""

# system module
import logging

# community module
from flask import Blueprint, Response, request

# project module
from circle_core.models import NoResultFound, User

from ..app import check_login

download = Blueprint('download', __name__)
logger = logging.getLogger(__name__)


@download.before_request
def before_request():
    """リクエスト前に呼ばれる."""
    token = request.args.get('access_token', None)
    if token:
        request.headers.environ['HTTP_AUTHORIZATION'] = 'Baerer {}'.format(token)
        check_login()
        return

    auth = request.authorization
    if not auth or not check_auth(auth.username, auth.password):
        return authenticate()


def check_auth(username, password):
    """パスワードをチェックする.

    :param str username: アカウント名
    :param str password: 平文パスワード
    :return:
    :rtype: bool
    """
    try:
        user = User.query.filter_by(account=username).one()
    except NoResultFound:
        return False

    return user.is_password_matched(password)


def authenticate():
    """認証を行う.

    :rtype: Response
    """
    return Response(
        response='Authorization Required',
        status=401,
        headers={'WWW-Authenticate': 'Basic realm="Authorization Required"'}
    )
