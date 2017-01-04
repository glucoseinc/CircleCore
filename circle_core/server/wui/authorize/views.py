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
    return {'hello': 'IoT!'}
