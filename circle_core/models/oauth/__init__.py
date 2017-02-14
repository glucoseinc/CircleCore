# -*- coding: utf-8 -*-
import datetime
import json
import logging

import sqlalchemy as sa
from sqlalchemy import orm
from werkzeug import cached_property


from circle_core.constants import CRScope
from ..base import GUID, MetaDataBase, MetaDataSession, StringList, TextList


logger = logging.getLogger(__name__)
REDIS_GRANT_KEY_PREFIX = '_oauth:grant:'
REDIS_TOKEN_KEY_PREFIX = '_oauth:token:'


class OAuthClient(MetaDataBase):
    """OAuthのClient

    client_id: A random string
    client_secret: A random string
    client_type: A string represents if it is confidential
    redirect_uris: A list of redirect uris
    default_redirect_uri: One of the redirect uris
    default_scopes: Default scopes of the client
    But it could be better, if you implemented:

    allowed_grant_types: A list of grant types
    allowed_response_types: A list of response types
    validate_scopes: A function to validate scopes

    Response Typeについては http://oauth.jp/blog/2015/01/06/oauth2-multiple-response-type/ を参照
    """

    __tablename__ = 'oauth_clients'

    client_id = sa.Column(sa.String, nullable=False, primary_key=True, unique=True)
    client_secret = sa.Column(sa.Text, nullable=False)
    redirect_uris = sa.Column(TextList, nullable=False)
    default_redirect_uri = sa.Column(sa.String, nullable=False)
    default_scopes = sa.Column(StringList, nullable=False)
    allowed_grant_types = sa.Column(StringList, nullable=False)
    allowed_response_types = sa.Column(StringList, nullable=False)

    def validate_scopes(self, scopes):
        # TODO:ちゃんと実装する
        logger.debug('validate_scopes %r', scopes)
        return True


class OAuthGrant(MetaDataBase):
    """OAuthのToken手前のGrant
    """

    __tablename__ = 'oauth_grants'

    client_id = sa.Column(sa.String, sa.ForeignKey('oauth_clients.client_id'), nullable=False)
    code = sa.Column(sa.String, nullable=False, unique=True, primary_key=True)
    redirect_uri = sa.Column(sa.String, nullable=False)
    scopes = sa.Column(StringList, nullable=False)
    user_id = sa.Column(GUID, sa.ForeignKey('users.uuid'), nullable=False)
    expires_at = sa.Column(sa.DateTime, nullable=False)

    user = orm.relationship('User', backref=orm.backref('grants', cascade='all, delete-orphan'))

    def to_json(self):
        """GRANTのJSON用表現を返す"""
        return json.dumps({
            'client_id': self.client_id,
            'code': self.code,
            'redirect_uri': self.redirect_uri,
            'scopes': self.scopes,
            'user': self.user,
        })

    @classmethod
    def from_json(cls, data):
        """GRANTのJSON用表現からGrantを復元する"""
        d = json.loads(data)
        return cls(
            d['client_id'],
            d['code'],
            d['redirect_uri'],
            d['scopes'],
            d['user'],
        )

    def delete(self):
        """Grantをストレージ(Redisから)削除する"""
        with MetaDataSession.begin():
            MetaDataSession.delete(self)


class OAuthToken(MetaDataBase):
    """OAuthのToken

    access_token: A string token
    refresh_token: A string token
    client_id: ID of the client
    scopes: A list of scopes
    expires: A datetime.datetime object
    user: The user object
    delete: A function to delete itself
    """

    __tablename__ = 'oauth_tokens'

    access_token = sa.Column(sa.String, nullable=False, unique=True, primary_key=True)
    refresh_token = sa.Column(sa.String, nullable=False, unique=True)
    client_id = sa.Column(sa.String, sa.ForeignKey('oauth_clients.client_id'), nullable=False)
    scopes = sa.Column(StringList, nullable=False)
    expires_at = sa.Column(sa.DateTime, nullable=False)
    user_id = sa.Column(GUID, sa.ForeignKey('users.uuid'), nullable=False)

    user = orm.relationship('User', backref=orm.backref('tokens', cascade='all, delete-orphan'))

    @property
    def expires(self):
        return self.expires_at

    def delete(self):
        """tokenの情報をMetadataDBから削除する"""
        with MetaDataSession.begin():
            MetaDataSession.delete(self)

            logger.debug('Delete token %s:%s', self.access_token, self.refresh_token)

    def to_json(self):
        """tokenのJSON表現を返す"""
        return json.dumps({
            'access_token': self.access_token,
            'refresh_token': self.refresh_token,
            'client_id': self.client_id,
            'scopes': self.scopes,
            'expires': self.expires.isoformat('T'),
            'user': self.user,
        })

    @classmethod
    def from_json(cls, data):
        """tokenのJSON表現からTokenを復元"""
        d = json.loads(data)
        return cls(
            d['access_token'],
            d['refresh_token'],
            d['client_id'],
            d['scopes'],
            datetime.datetime.strptime(d['expires'], '%Y-%m-%dT%H:%M:%S.%f'),
            d['user'],
        )
