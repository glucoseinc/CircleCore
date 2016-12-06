# -*- coding: utf-8 -*-

# system module
from __future__ import absolute_import

# community module
from redis import ConnectionError, Redis
from six import PY3

# project module
from .base import MetadataError, MetadataReader, MetadataWriter
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


class MetadataRedis(MetadataReader, MetadataWriter):
    """MetadataRedisオブジェクト.

    :param RedisClient redis_client: Redisクライアント
    """

    stringified_type = 'Redis'

    def __init__(self, redis_client):
        """init.

        :param RedisClient redis_client: Redisクライアント
        """
        super(MetadataRedis, self).__init__()
        self.redis_client = redis_client

    @classmethod
    def parse_url_scheme(cls, url_scheme):
        try:
            redis_client = RedisClient.from_url(url_scheme)
            redis_client.ping()
        except ConnectionError:
            raise MetadataError('Cannot connect to Redis server.')

        return MetadataRedis(redis_client)

    @property
    def schemas(self):
        schemas = []
        keys = [key for key in self.redis_client.keys() if Schema.is_key_matched(key)]
        for key in keys:
            if self.redis_client.type(key) == 'hash':
                fields = self.redis_client.hgetall(key)  # type: Dict[str, Any]
                schemas.append(Schema(**fields))
        return schemas

    @property
    def devices(self):
        devices = []
        keys = [key for key in self.redis_client.keys() if Device.is_key_matched(key)]
        for key in keys:
            if self.redis_client.type(key) == 'hash':
                fields = self.redis_client.hgetall(key)  # type: Dict[str, Any]
                devices.append(Device(**fields))
        return devices

    def register_schema(self, schema):
        mapping = {
            'uuid': schema.uuid,
            'display_name': schema.display_name,
            'properties': schema.stringified_properties
        }

        self.redis_client.hmset(schema.storage_key, mapping)

    def unregister_schema(self, schema):
        self.redis_client.delete(schema.storage_key)

    def register_device(self, device):
        mapping = {
            'uuid': device.uuid,
            'display_name': device.display_name,
            'schema_uuid': device.schema_uuid,
            'properties': device.stringified_properties
        }

        self.redis_client.hmset(device.storage_key, mapping)

    def unregister_device(self, device):
        self.redis_client.delete(device.storage_key)

    def update_device(self, device):
        self.register_device(device)
