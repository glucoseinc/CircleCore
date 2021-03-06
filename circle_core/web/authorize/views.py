# -*- coding: utf-8 -*-
"""認証関連APIの実装."""

# system module
import logging
import time

# community module
from flask import abort, g, redirect, render_template, request, session, url_for

# project module
from circle_core.constants import CRScope
from circle_core.exceptions import AuthorizationError
from circle_core.models import NoResultFound, User

from .core import authorize, oauth
from ..utils import api_jsonify

SESSION_KEY_USER = 'user'
SESSION_KEY_NONCE = 'nonce'
logger = logging.getLogger(__name__)


def _login(user):
    """ログインする."""
    session[SESSION_KEY_USER] = str(user.uuid)


def _logout():
    """web（というかcookie）からログアウトする."""
    session.pop(SESSION_KEY_USER, None)


@authorize.before_request
def before_request():
    """ログイン確認."""
    g.user = None
    user_uuid = session.get(SESSION_KEY_USER)
    if not user_uuid:
        return

    user = User.query.get(user_uuid)
    if not user:
        return

    g.user = user


authorize.add_url_rule('/oauth/callback', endpoint='oauth_callback', build_only=True)


@authorize.route('/oauth/authorize', methods=['GET', 'POST'])
@oauth.authorize_handler
def oauth_authorize(*args, **kwargs):
    """OAuth認証の確認を行う."""
    if not g.user:
        logger.info('oauth_authorize: user is not authorized')
        return redirect(url_for('.oauth_login', redirect=request.full_path))

    if request.method == 'GET':
        nonce = time.time()
        session[SESSION_KEY_NONCE] = nonce
        logger.info('oauth_authorize: show authorize page, nonce=%r', nonce)
        return render_template('oauth/authorize.html', nonce=nonce, **kwargs)

    assert request.method == 'POST'

    # check nonce
    saved_nonce = str(session.pop(SESSION_KEY_NONCE, None))
    if request.form['nonce'] != saved_nonce:
        # nonce not matched
        _logout()
        return False

    return True


@authorize.route('/oauth/login', methods=['GET', 'POST'])
def oauth_login():
    """通常のWebログイン."""
    if request.method == 'GET':
        redirect_to = request.args['redirect']
        if not redirect_to.startswith('/'):
            # このサイト内のpathでなければエラーに
            raise abort(400)
        return render_template('oauth/login.html', redirect_to=redirect_to)

    assert request.method == 'POST'

    redirect_to = request.form['redirect']
    if not redirect_to.startswith('/'):
        # このサイト内のpathでなければエラーに
        raise abort(400)

    try:
        user = _find_user_by_password(request.form['account'], request.form['password'])
    except AuthorizationError:
        logger.info('Login failed %s', request.form['account'])
        return render_template('oauth/login.html', redirect_to=redirect_to, is_failed=True)

    # ログイン処理
    logger.info('Logging in %s(%s), redirect to %s', user.account, user.uuid, redirect_to)
    _login(user)
    return redirect(redirect_to)


def _find_user_by_password(account, password):
    """account/passwordが適合するユーザを取得する.

    :param str account: アカウント名
    :param str password: 平文パスワード
    :return: User
    :rtype: User
    """

    # TODO: コントローラを作成して移動
    try:
        user = User.query.filter_by(account=account).one()
    except NoResultFound:
        raise AuthorizationError('user not found', account)

    if not user.is_password_matched(password):
        raise AuthorizationError('password did not matched')

    return user


@authorize.route('/oauth/errors')
def oauth_error():
    error = request.args.get('error', 'error')
    return render_template('oauth/errors.html', error=error)


@authorize.route('/oauth/token', methods=['POST'])
@oauth.token_handler
def access_token():
    _logout()


@authorize.route('/oauth/revoke', methods=['POST'])
@oauth.revoke_handler
def revoke_token():
    _logout()


@oauth.invalid_response
def invalid_require_oauth(req):
    status = 401
    if req.error_message in ('Bearer token not found.', 'Bearer token is expired.'):
        status = 403
    return api_jsonify(message=req.error_message, _status=status)


# Scopeテスト用関数群
for _scope in [s.value for s in CRScope] + ['bad-scope']:

    @authorize.route('/api/oauth/scope_test/' + _scope, endpoint='test_scope_{}'.format(_scope))
    @oauth.require_oauth(_scope)
    def test_scope_view():
        return api_jsonify({'scope': _scope})
