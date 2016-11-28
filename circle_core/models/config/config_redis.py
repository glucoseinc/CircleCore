# -*- coding: utf-8 -*-

# community module
from redis import ConnectionError, Redis
from six import PY3

# project module
from .config_base import Config, ConfigError
from ..device import Device
from ..schema import Schema

if PY3:
    from typing import Any, Dict


class RedisClient(Redis):
    """Redisクライアント."""

    def parse_response(self, connection, command_name, **options):
        """Parses a response from the Redis server."""
        def decoded(word):
            """bytesはstrに変換する."""
            return word.decode('utf-8') if isinstance(word, bytes) else word

        response = super(RedisClient, self).parse_response(connection, command_name, **options)

        if PY3:
            if isinstance(response, bytes):
                return decoded(response)
            elif isinstance(response, list):
                return [decoded(resp) for resp in response]
            elif isinstance(response, dict):
                return {decoded(k): decoded(v) for k, v in response.items()}
        return response


class ConfigRedis(Config):
    """ConfigRedisオブジェクト.

    :param RedisClient redis_client: Redisクライアント
    """

    stringified_type = 'Redis'

    def __init__(self, redis_client):
        """init.

        :param RedisClient redis_client: Redisクライアント
        """
        super(ConfigRedis, self).__init__()
        self.redis_client = redis_client

        self.instantiate_all_schemas()
        self.instantiate_all_devices()

    @classmethod
    def parse_url_scheme(cls, url_scheme):
        """RedisからConfigオブジェクトを生成する.

        :param str url_scheme: URLスキーム
        :return: ConfigRedisオブジェクト
        :rtype: ConfigRedis
        """
        try:
            redis_client = RedisClient.from_url(url_scheme)
            redis_client.ping()
        except ConnectionError:
            raise ConfigError('Cannot connect to Redis server.')

        return ConfigRedis(redis_client)

    @property
    def readable(self):
        return True

    @property
    def writable(self):
        return True

    def instantiate_all_schemas(self):
        self.schemas = []
        keys = [key for key in self.redis_client.keys() if Schema.is_key_matched(key)]
        for key in keys:
            if self.redis_client.type(key) == 'hash':
                fields = self.redis_client.hgetall(key)  # type: Dict[str, Any]
                self.schemas.append(Schema(**fields))

    def register_schema(self, schema):
        mapping = {
            'uuid': schema.uuid,
            'display_name': schema.display_name,
        }
        for i, prop in enumerate(schema.properties, start=1):
            mapping['key{}'.format(i)] = prop.name
            mapping['type{}'.format(i)] = prop.type

        key = 'schema_{}'.format(schema.uuid)
        self.redis_client.hmset(key, mapping)

    def unregister_schema(self, schema):
        key = 'schema_{}'.format(schema.uuid)
        self.redis_client.delete(key)

    def instantiate_all_devices(self):
        self.devices = []
        keys = [key for key in self.redis_client.keys() if Device.is_key_matched(key)]
        for key in keys:
            if self.redis_client.type(key) == 'hash':
                fields = self.redis_client.hgetall(key)  # type: Dict[str, Any]
                self.devices.append(Device(**fields))

    def register_device(self, device):
        mapping = {
            'uuid': device.uuid,
            'display_name': device.display_name,
            'schema_uuid': device.schema_uuid,
        }
        for i, prop in enumerate(device.properties, start=1):
            mapping['property{}'.format(i)] = prop.name
            mapping['value{}'.format(i)] = prop.value

        key = 'device_{}'.format(device.uuid)
        self.redis_client.hmset(key, mapping)

    def unregister_device(self, device):
        key = 'device_{}'.format(device.uuid)
        self.redis_client.delete(key)

    def update_device(self, device):
        key = 'device_{}'.format(device.uuid)
        hkeys = [hkey for hkey in self.redis_client.hkeys(key)
                 if hkey.startswith('property') or hkey.startswith('value')]
        self.redis_client.hdel(key, *hkeys)
        self.register_device(device)
