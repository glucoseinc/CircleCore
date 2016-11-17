#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Schema Model."""

# system module
import re

# community module
from six import PY3

# project module
from ..controllers.redis_client import RedisClient

if PY3:
    from typing import Dict, List, Optional


class Schema(object):
    """Schemaオブジェクト.

    :param str uuid: Schema UUID
    :param str display_name: 表示名
    :param properties: プロパティ
    :type properties: Dict[str, str]
    """

    def __init__(self, uuid, display_name, **kwargs):
        """init.

        :param str uuid: Schema UUID
        :param str display_name: 表示名
        """
        self.uuid = uuid
        self.display_name = display_name
        self.properties = {}
        property_keys = [k for k in kwargs.keys() if k.startswith('key')]
        for property_key in property_keys:
            idx = property_key[3:]
            property_type = 'type' + idx
            if property_type in kwargs.keys():
                self.properties[kwargs[property_key]] = kwargs[property_type]

    @classmethod
    def init_from_redis(cls, redis_client, num):
        """Redisからインスタンス化する.

        :param RedisClient redis_client: Redisクライアント
        :param int num: キーナンバー
        :return: Schemaオブジェクト
        :rtype: Optional[Schema]
        """
        key = 'schema{}'.format(num)
        if key not in redis_client.keys():
            return None
        if redis_client.type(key) != 'hash':
            return None
        fields = redis_client.hgetall(key)
        return Schema(**fields)

    @classmethod
    def init_all_items_from_redis(cls, redis_client):
        """Redisから全てのSchemaオブジェクトをインスタンス化する.

        :param RedisClient redis_client: Redisクライアント
        :return: 全てのSchemaオブジェクト
        :rtype: List[Schema]
        """
        keys = [key for key in redis_client.keys() if re.match(r'^schema\d+', key)]
        instances = []
        for key in keys:
            if redis_client.type(key) == 'hash':
                fields = redis_client.hgetall(key)
                instances.append(Schema(**fields))
        return instances
