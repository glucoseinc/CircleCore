# -*- coding: utf-8 -*-
"""OAuth."""

# system module
import datetime
import json
import logging

# community module
import sqlalchemy as sa
from sqlalchemy import orm

# project module
from ..base import GUID, MetaDataBase, MetaDataSession, StringList, TextList

# type annotation
try:
    from ..user import User
except ImportError:
    pass

logger = logging.getLogger(__name__)
REDIS_GRANT_KEY_PREFIX = '_oauth:grant:'
REDIS_TOKEN_KEY_PREFIX = '_oauth:token:'


class OAuthClient(MetaDataBase):
    """OAuthのClient.
    Response Typeについては http://oauth.jp/blog/2015/01/06/oauth2-multiple-response-type/ を参照

    :param str client_id: A random string
    :param str client_secret: A random string
    :param str redirect_uris: A list of redirect uris
    :param str default_redirect_uri: One of the redirect uris
    :param str default_scopes: Default scopes of the client
    :param str allowed_grant_types: A list of grant types
    :param str allowed_response_types: A list of response types
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
        """A function to validate scopes.

        :param str scopes: scopes
        :return: result
        :rtype: bool
        """
        # TODO:ちゃんと実装する
        logger.debug('validate_scopes %r', scopes)
        return True


class OAuthGrant(MetaDataBase):
    """OAuthのToken手前のGrant.

    :param str client_id:
    :param str code:
    :param str redirect_uri:
    :param str scopes:
    :param str user_id:
    :param datetime.datetime expires_at:
    :param User user:
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
        """このモデルのJSON表現を返す.

        :return: JSON表現
        :rtype: str
        """
        return json.dumps(
            {
                'client_id': self.client_id,
                'code': self.code,
                'redirect_uri': self.redirect_uri,
                'scopes': self.scopes,
                'user': self.user,
            }
        )

    @classmethod
    def from_json(cls, data):
        """JSON表現からモデルを生成する.

        :param str data: JSON表現
        :return: OAuthGrantオブジェクト
        :rtype: OAuthGrant
        """
        d = json.loads(data)
        return cls(
            d['client_id'],
            d['code'],
            d['redirect_uri'],
            d['scopes'],
            d['user'],
        )

    def delete(self):
        """Grantを削除する."""
        with MetaDataSession.begin():
            MetaDataSession.delete(self)


class OAuthToken(MetaDataBase):
    """OAuthのToken.

    :param str access_token: A string token
    :param str refresh_token: A string token
    :param str client_id: ID of the client
    :param str scopes: A list of scopes
    :param datetime.datetime expires_at: A datetime.datetime object
    :param str user_id: The user object
    :param User user:
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
        """expires_atのalias.

        :return: expires
        :rtype: datetime.datetime
        """
        return self.expires_at

    def delete(self):
        """tokenの情報をMetadataDBから削除する."""
        with MetaDataSession.begin():
            MetaDataSession.delete(self)

            logger.debug('Delete token %s:%s', self.access_token, self.refresh_token)

    def to_json(self):
        """このモデルのJSON表現を返す.

        :return: JSON表現
        :rtype: str
        """
        return json.dumps(
            {
                'access_token': self.access_token,
                'refresh_token': self.refresh_token,
                'client_id': self.client_id,
                'scopes': self.scopes,
                'expires': self.expires.isoformat('T'),
                'user': self.user,
            }
        )

    @classmethod
    def from_json(cls, data):
        """JSON表現からモデルを生成する.

        :param str data: JSON表現
        :return: OAuthGrantオブジェクト
        :rtype: OAuthGrant
        """
        d = json.loads(data)
        return cls(
            d['access_token'],
            d['refresh_token'],
            d['client_id'],
            d['scopes'],
            datetime.datetime.strptime(d['expires'], '%Y-%m-%dT%H:%M:%S.%f'),
            d['user'],
        )
