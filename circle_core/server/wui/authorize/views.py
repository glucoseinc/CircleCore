# -*- coding: utf-8 -*-

"""認証関連APIの実装."""

from flask import request, render_template

from .core import authorize, oauth
from ..utils import api_jsonify


@authorize.route('/oauth/authorize', methods=['GET', 'POST'])
@oauth.authorize_handler
def oauth_authorize(*args, **kwargs):
    if request.method == 'GET':
        return render_template('oauth/authorize.html', **kwargs)
    return request.form.get('confirmed', 'no') == 'yes'


@authorize.route('/oauth/errors')
def oauth_error():
    error = request.args.get('error', 'error')
    return render_template('oauth/errors.html', error=error)


@authorize.route('/oauth/token', methods=['POST'])
@oauth.token_handler
def access_token():
    pass


@authorize.route('/oauth/revoke', methods=['POST'])
@oauth.revoke_handler
def revoke_token():
    pass


@oauth.invalid_response
def invalid_require_oauth(req):
    status = 401
    if req.error_message == 'Bearer token not found.':
        status = 403
    return api_jsonify(message=req.error_message, _status=status)


# テスト用関数群
@authorize.route('/api/oauth/scope_test/user')
@oauth.require_oauth('user')
def test_scope_user():
    return api_jsonify({'scope': 'user'})


@authorize.route('/api/oauth/scope_test/schema+r')
@oauth.require_oauth('schema+r', 'schema+rw')
def test_scope_schema_read():
    return api_jsonify({'scope': 'schema+r'})


@authorize.route('/api/oauth/scope_test/schema+rw')
@oauth.require_oauth('schema+rw')
def test_scope_schema_readwrite():
    return api_jsonify({'scope': 'schema+rw'})


@authorize.route('/api/oauth/scope_test/bad-scope')
@oauth.require_oauth('bad-scope')
def test_scope_schema_hgoehoge():
    return api_jsonify({'scope': 'bad-scope'})
