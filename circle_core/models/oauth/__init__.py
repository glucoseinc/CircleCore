# -*- coding: utf-8 -*-
"""OAuth."""

# system module
import datetime
import json
import logging
from typing import TYPE_CHECKING

# community module
import sqlalchemy as sa
from sqlalchemy import orm

# project module
from ..base import GUID, MetaDataBase, MetaDataSession, StringList, TextList

# type annotation
if TYPE_CHECKING:
    from ..user import User

logger = logging.getLogger(__name__)
REDIS_GRANT_KEY_PREFIX = '_oauth:grant:'
REDIS_TOKEN_KEY_PREFIX = '_oauth:token:'


class OAuthClient(MetaDataBase):
    """OAuthのClient.
    Response Typeについては http://oauth.jp/blog/2015/01/06/oauth2-multiple-response-type/ を参照

    Attributes:
        client_id (str): A random string
        client_secret (str): A random string
        redirect_uris (str): A list of redirect uris
        default_redirect_uri (str): One of the redirect uris
        default_scopes (str): Default scopes of the client
        allowed_grant_types (str): A list of grant types
        allowed_response_types (str): A list of response types
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

        Args:
            scopes (str): scopes

        Returns:
            bool: scopeの値が間違ってなければ
        """
        # TODO:ちゃんと実装する
        logger.debug('validate_scopes %r', scopes)
        return True


class OAuthGrant(MetaDataBase):
    """OAuthのToken手前のGrant.

    Attributes:
        client_id (str):
        code (str):
        redirect_uri (str):
        scopes (str):
        user_id (str):
        expires_at (datetime.datetime):
        user (circle_core.models.User):
    """

    __tablename__ = 'oauth_grants'

    client_id = sa.Column(sa.String, sa.ForeignKey('oauth_clients.client_id'), nullable=False)
    code = sa.Column(sa.String, nullable=False, unique=True, primary_key=True)
    redirect_uri = sa.Column(sa.String, nullable=False)
    scopes = sa.Column(StringList, nullable=False)
    user_id = sa.Column(GUID, sa.ForeignKey('users.uuid'), nullable=False)
    expires_at = sa.Column(sa.DateTime, nullable=False)

    user = orm.relationship('User', backref=orm.backref('grants', cascade='all, delete-orphan'))

    def to_json(self) -> str:
        """このモデルのJSON表現を返す.

        Returns:
            str: JSON表現
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
    def from_json(cls, data: str) -> 'OAuthGrant':
        """JSON表現からモデルを生成する.

        Args:
            data (str): JSON表現

        Returns:
            circle_core.models.OAuthGrant: OAuthGrantオブジェクト
        """
        d = json.loads(data)
        return cls(
            d['client_id'],
            d['code'],
            d['redirect_uri'],
            d['scopes'],
            d['user'],
        )

    def delete(self) -> None:
        """Grantを削除する."""
        with MetaDataSession.begin():
            MetaDataSession.delete(self)


class OAuthToken(MetaDataBase):
    """OAuthのToken.

    Attributes:
        access_token (str): A string token
        refresh_token (str): A string token
        client_id (str): ID of the client
        scopes (str): A list of scopes
        expires_at (datetime.datetime): A datetime.datetime object
        user_id (str): The user object
        user (circle_core.models.User):
    """
    user: 'User'

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

        Returns:
            datetime.datetime: expires
        """
        return self.expires_at

    def delete(self):
        """tokenの情報をMetadataDBから削除する."""
        with MetaDataSession.begin():
            MetaDataSession.delete(self)

            logger.debug('Delete token %s:%s', self.access_token, self.refresh_token)

    def to_json(self):
        """このモデルのJSON表現を返す.

        Returns:
            str: JSON表現
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

        Attributes:
            data (str): JSON表現

        Args:
            OAuthGrant: OAuthGrantオブジェクト
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
