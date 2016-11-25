# -*- coding: utf-8 -*-

"""Schema Model."""

# system module
import re

# community module
from six import PY3

# project module
from .redis_client import RedisClient

if PY3:
    from typing import Any, Dict, List, Optional


class SchemaProperty(object):
    """SchemaPropertyオブジェクト.

    :param str name: 属性名
    :param str type: タイプ
    """

    def __init__(self, name, property_type):
        """init.

        :param str name: キー
        :param str property_type: タイプ
        """
        self.name = name
        self.type = property_type


class Schema(object):
    """Schemaオブジェクト.

    :param str uuid: Schema UUID
    :param Optional[str] display_name: 表示名
    :param List[SchemaProperty] properties: プロパティ
    """

    def __init__(self, uuid, display_name=None, **kwargs):
        """init.

        :param str uuid: Schema UUID
        :param Optional[str] display_name: 表示名
        """
        self.uuid = uuid
        self.display_name = display_name
        self.properties = []
        property_names = sorted([k for k in kwargs.keys() if k.startswith('key')])
        for property_name in property_names:
            idx = property_name[3:]
            property_type = 'type' + idx
            if property_type in kwargs.keys():
                self.properties.append(SchemaProperty(kwargs[property_name], kwargs[property_type]))

    @property
    def stringified_properties(self):
        """プロパティを文字列化する.

        :return: 文字列化プロパティ
        :rtype: str
        """
        strings = []
        for prop in self.properties:
            strings.append('{}:{}'.format(prop.name, prop.type))
        return ', '.join(strings)

    # TODO: Redis関係は分離するか？

    @classmethod
    def init_from_redis(cls, redis_client, uuid):
        """Redisからインスタンス化する.

        :param RedisClient redis_client: Redisクライアント
        :param str uuid: Schema UUID
        :return: Schemaオブジェクト
        :rtype: Optional[Schema]
        """
        key = 'schema_{}'.format(uuid)
        if key not in redis_client.keys():
            return None
        if redis_client.type(key) != 'hash':
            return None
        fields = redis_client.hgetall(key)  # type: Dict[str, Any]
        return Schema(**fields)

    @classmethod
    def init_all_items_from_redis(cls, redis_client):
        """Redisから全てのSchemaオブジェクトをインスタンス化する.

        :param RedisClient redis_client: Redisクライアント
        :return: 全てのSchemaオブジェクト
        :rtype: List[Schema]
        """
        # TODO: UUIDのマッチ部分
        keys = [key for key in redis_client.keys() if re.match(r'^schema_[0-9a-fA-F-]+', key)]
        instances = []
        for key in keys:
            if redis_client.type(key) == 'hash':
                fields = redis_client.hgetall(key)  # type: Dict[str, Any]
                instances.append(Schema(**fields))
        return instances

    def register_to_redis(self, redis_client):
        """Redisに登録する.

        :param RedisClient redis_client: Redisクライアント
        """
        mapping = {
            'uuid': self.uuid,
            'display_name': self.display_name,
        }
        for i, prop in enumerate(self.properties, start=1):
            mapping['key{}'.format(i)] = prop.name
            mapping['type{}'.format(i)] = prop.type

        key = 'schema_{}'.format(self.uuid)
        redis_client.hmset(key, mapping)

    def unregister_from_redis(self, redis_client):
        """Redisから削除する.

        :param RedisClient redis_client: Redisクライアント
        """
        key = 'schema_{}'.format(self.uuid)
        redis_client.delete(key)
