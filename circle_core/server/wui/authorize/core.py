# -*- coding: utf-8 -*-
"""Flask oauth implementation."""
import datetime

# community module
from flask import Blueprint, current_app, g
from flask_oauthlib.provider import OAuth2Provider

from .models import OAuthClient, OAuthGrant, OAuthToken
from circle_core.constants import CRScope


authorize = Blueprint('authorize', __name__)
oauth = OAuth2Provider()
oauth_clients = {}


WEBUICLIENT_CLIENT_ID = '8F9A5449-F219-4BC4-9EA6-5F4C3100CD25'
webui_client = OAuthClient(
    WEBUICLIENT_CLIENT_ID,
    '3f82ad86ff167cebc39bf735533efe080b596f4ce343e4f51fd6c760a9835ccb' +
    '6ff76df5d2e72489b30d07ce81a273a6ea4128f98412f4b6027245c76cd0a098',
    ['http://localhost:5000'],
    'http://localhost:5000',
    [s.value for s in CRScope],
    ['password', 'authorization_code', 'refresh_token'],
    ['code']
)


def register_client(client):
    oauth_clients[client.client_id] = client
register_client(webui_client)


# oauth handlers
@oauth.clientgetter
def load_client(client_id):
    return oauth_clients.get(client_id)


@oauth.grantgetter
def load_grant(client_id, code):
    grant = OAuthGrant.load(_get_redis_client(), client_id, code)
    return grant


@oauth.grantsetter
def save_grant(client_id, code, request, *args, **kwargs):
    assert g.user

    scopes = request.scopes[:]

    if not g.user.is_admin():
        # adminでなければ`user` scopeを落とす
        try:
            scopes.remove(CRScope.USER_RW.value)
        except ValueError:
            pass

    grant = OAuthGrant(
        client_id,
        code['code'],
        request.redirect_uri,
        scopes,
        str(g.user.uuid),
    )
    grant.save(_get_redis_client(), 120)  # 2minsでexpire


@oauth.tokengetter
def load_token(access_token=None, refresh_token=None):
    token = None
    if access_token:
        token = OAuthToken.load_token_by_access_token(_get_redis_client(), access_token)
    elif refresh_token:
        token = OAuthToken.load_token_by_refresh_token(_get_redis_client(), refresh_token)

    return token


@oauth.tokensetter
def save_token(token, request, *args, **kwargs):
    # TODO: 古いTokenを消したいけどRedisではダルい
    expires_in = token.get('expires_in')
    expires = datetime.datetime.utcnow() + datetime.timedelta(seconds=expires_in)

    token_obj = OAuthToken(
        token['access_token'], token['refresh_token'],
        request.client.client_id,
        token['scope'],
        expires,
        request.user)
    token_obj.save(_get_redis_client())


def _get_redis_client():
    """
    汚い... metadataからRedisへの接続を得る
    """
    metadata = current_app.config['METADATA']
    # TODO:metadataがiniファイルだったらどうしよう?
    return metadata.redis_client
