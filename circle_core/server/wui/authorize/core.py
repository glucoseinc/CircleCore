# -*- coding: utf-8 -*-
"""Flask oauth implementation."""
import datetime
import logging

# community module
from flask import Blueprint, current_app, g, url_for
from flask_oauthlib.provider import OAuth2Provider

from circle_core.constants import CRScope
from circle_core.models import MetaDataSession, NoResultFound, OAuthClient, OAuthGrant, OAuthToken


authorize = Blueprint('authorize', __name__)
logger = logging.getLogger(__name__)
oauth = OAuth2Provider()
WEBUICLIENT_CLIENT_ID = '8F9A5449-F219-4BC4-9EA6-5F4C3100CD25'


def initialize_oauth():
    """OAuth関連の起動時の初期化を行う"""

    # WebUI用のOAuthClientを登録する
    client = OAuthClient.query.get(WEBUICLIENT_CLIENT_ID)

    with MetaDataSession.begin():
        redirect_uri = url_for('authorize.oauth_callback', _external=True)
        if client:
            client.redirect_uris = [redirect_uri]
            client.default_redirect_uri = redirect_uri
            logger.debug('Updating WebUI OAuth Client: redirect_uri to `%s`', redirect_uri)
        else:
            client = OAuthClient(**{
                'client_id': WEBUICLIENT_CLIENT_ID,
                'client_secret': (
                    '3f82ad86ff167cebc39bf735533efe080b596f4ce343e4f51fd6c760a9835ccb'
                    '6ff76df5d2e72489b30d07ce81a273a6ea4128f98412f4b6027245c76cd0a098'
                ),
                'redirect_uris': [redirect_uri],
                'default_redirect_uri': redirect_uri,
                'default_scopes': ['schema+rw', 'user+rw'],
                'allowed_grant_types': ['password', 'authorization_code', 'refresh_token'],
                'allowed_response_types': ['code'],
            })
            logger.debug('Creating WebUI OAuth Client: redirect_uri to `%s`', redirect_uri)
        MetaDataSession.add(client)


@oauth.clientgetter
def load_client(client_id):
    return OAuthClient.query.get(client_id)


@oauth.grantgetter
def load_grant(client_id, code):
    try:
        now = datetime.datetime.utcnow()
        return (
            OAuthGrant.query
            .filter_by(client_id=client_id, code=code)
            .filter(OAuthGrant.expires_at > now)
            .one()
        )
    except NoResultFound:
        return None


@oauth.grantsetter
def save_grant(client_id, code, request, *args, **kwargs):
    assert g.user

    scopes = set(request.scopes[:])

    if not g.user.is_admin():
        # adminでなければ`user` scopeを落とす
        try:
            scopes.discard(CRScope.USER_RW.value)
        except ValueError:
            pass
        scopes.add(CRScope.USER_R.value)

    with MetaDataSession.begin():
        grant = OAuthGrant(
            client_id=client_id,
            code=code['code'],
            redirect_uri=request.redirect_uri,
            scopes=scopes,
            user_id=g.user.uuid,
            expires_at=datetime.datetime.utcnow() + datetime.timedelta(seconds=120),
        )
        MetaDataSession.add(grant)


@oauth.tokengetter
def load_token(access_token=None, refresh_token=None):
    query = OAuthToken.query
    if access_token:
        query = query.filter_by(access_token=access_token)
    if refresh_token:
        query = query.filter_by(refresh_token=refresh_token)

    try:
        token = query.one()
    except NoResultFound:
        token = None
    logger.debug('Load token %s:%s -> %r', access_token, refresh_token, token)
    return token


@oauth.tokensetter
def save_token(token, request, *args, **kwargs):
    expires_in = token.get('expires_in')
    expires = datetime.datetime.utcnow() + datetime.timedelta(seconds=expires_in)

    with MetaDataSession.begin():
        token_obj = OAuthToken(
            access_token=token['access_token'],
            refresh_token=token['refresh_token'],
            client_id=request.client.client_id,
            scopes=token['scope'].split(' '),
            expires_at=expires,
            user_id=request.user.uuid)
        MetaDataSession.add(token_obj)

        logger.debug('Save token %s:%s', token_obj.access_token, token_obj.refresh_token)
