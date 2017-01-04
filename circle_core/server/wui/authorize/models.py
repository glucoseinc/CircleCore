# -*- coding: utf-8 -*-
import json
import datetime

REDIS_GRANT_KEY_PREFIX = '_oauth:grant:'
REDIS_TOKEN_KEY_PREFIX = '_oauth:token:'


class OAuthClient(object):
    '''
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

    '''
    def __init__(
            self, client_id, client_secret, redirect_uris, default_redirect_uri, default_scopes,
            allowed_grant_types, allowed_response_types):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uris = redirect_uris
        self.default_redirect_uri = default_redirect_uri
        self.default_scopes = default_scopes
        self.allowed_grant_types = allowed_grant_types
        self.allowed_response_types = allowed_response_types


class OAuthGrant(object):
    def __init__(self, client_id, code, redirect_uri, scopes, user):
        self.client_id = client_id
        self.code = code
        self.redirect_uri = redirect_uri
        self.scopes = scopes
        self.user = user

    def save(self, redis_client, expires):
        key = self.make_key(self.client_id, self.code)
        redis_client.set(key, self.to_json())
        redis_client.expire(key, expires)

    @classmethod
    def load(cls, redis_client, client_id, code):
        key = cls.make_key(client_id, code)
        data = redis_client.get(key)
        if data:
            return cls.from_json(data)

    def to_json(self):
        return json.dumps({
            'client_id': self.client_id,
            'code': self.code,
            'redirect_uri': self.redirect_uri,
            'scopes': self.scopes,
            'user': self.user,
        })

    @classmethod
    def from_json(cls, data):
        d = json.loads(data)
        return cls(
            d['client_id'],
            d['code'],
            d['redirect_uri'],
            d['scopes'],
            d['user'],
        )

    @classmethod
    def make_key(cls, client_id, code):
        return REDIS_GRANT_KEY_PREFIX + '{}:{}'.format(client_id, code)

    def delete(self):
        print('!! delete grant', self.client_id, self.code)
        from .core import _get_redis_client
        redis_client = _get_redis_client()
        redis_client.delete(self.make_key(self.client_id, self.code))


class OAuthToken(object):
    '''
    access_token: A string token
    refresh_token: A string token
    client_id: ID of the client
    scopes: A list of scopes
    expires: A datetime.datetime object
    user: The user object
    delete: A function to delete itself
    '''

    def __init__(self, access_token, refresh_token, client_id, scopes, expires, user):
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.client_id = client_id
        self.scopes = scopes
        self.expires = expires
        self.user = user

    def save(self, redis_client):
        data = self.to_json()
        redis_client.set(self.make_key_by_access_token(self.access_token), data)
        redis_client.set(self.make_key_by_refresh_token(self.refresh_token), data)

    def delete(self):
        from .core import _get_redis_client
        redis_client = _get_redis_client()
        redis_client.delete(self.make_key_by_access_token(self.access_token))
        redis_client.delete(self.make_key_by_refresh_token(self.refresh_token))

    def to_json(self):
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
        d = json.loads(data)
        return cls(
            d['access_token'],
            d['refresh_token'],
            d['client_id'],
            d['scopes'],
            datetime.datetime.strptime(d['expires'], '%Y-%m-%dT%H:%M:%S.%fZ'),
            d['user'],
        )

    @classmethod
    def load_token_by_access_token(cls, redis_client, access_token):
        data = redis_client.get(cls.make_key_by_access_token(access_token))
        if data:
            return cls.from_json(data)

    @classmethod
    def load_token_by_refresh_token(cls, redis_client, refresh_token):
        data = redis_client.get(cls.make_key_by_refresh_token(refresh_token))
        if data:
            return cls.from_json(data)

    @classmethod
    def make_key_by_access_token(cls, access_token):
        return REDIS_TOKEN_KEY_PREFIX + 'access_token:{}'.format(access_token)

    @classmethod
    def make_key_by_refresh_token(cls, refresh_token):
        return REDIS_TOKEN_KEY_PREFIX + 'refresh_token:{}'.format(refresh_token)
