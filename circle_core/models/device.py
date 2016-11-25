# -*- coding: utf-8 -*-

"""Device Model."""

# system module
import re

# community module
from six import PY3

# project module
from .redis_client import RedisClient

if PY3:
    from typing import Any, Dict, List, Optional, Tuple


class DeviceProperty(object):
    """DevicePropertyオブジェクト.

    :param str name: 属性名
    :param str value: 属性値
    """

    def __init__(self, name, value):
        """init.

        :param str name: 属性名
        :param str value: 属性値
        """
        self.name = name
        self.value = value


class Device(object):
    """Deviceオブジェクト.

    :param str uuid: Device UUID
    :param Optional[str] display_name: 表示名
    :param str schema_uuid: Schema UUID
    :param List[DeviceProperty] properties: プロパティ
    """

    def __init__(self, uuid, schema_uuid, display_name=None, **kwargs):
        """init.

        :param str uuid; Device UUID
        :param str schema_uuid: Schema UUID
        :param Optional[str] display_name: 表示名
        """
        self.uuid = uuid
        self.schema_uuid = schema_uuid
        self.display_name = display_name
        self.properties = []
        property_names = sorted([k for k in kwargs.keys() if k.startswith('property')])
        for property_name in property_names:
            idx = property_name[8:]
            property_value = 'value' + idx
            if property_value in kwargs.keys():
                self.properties.append(DeviceProperty(kwargs[property_name], kwargs[property_value]))

    @property
    def stringified_properties(self):
        """プロパティを文字列化する.

        :return: 文字列化プロパティ
        :rtype: str
        """
        strings = []
        for prop in self.properties:
            strings.append('{}:{}'.format(prop.name, prop.value))
        return ', '.join(strings)

    def append_properties(self, name_and_values):
        """プロパティを追加する.

        :param List[Tuple[str, str]] name_and_values: 属性名と属性値のタプルのリスト
        """
        for name, value in name_and_values:
            for prop in self.properties:
                if prop.name == name:
                    prop.value = value
                    break
            else:
                self.properties.append(DeviceProperty(name, value))

    def remove_properties(self, names):
        """プロパティを除去する.

        :param List[str] names: 属性名リスト
        """
        self.properties = [prop for prop in self.properties if prop.name not in names]

    # TODO: Redis関係は分離するか？

    @classmethod
    def init_from_redis(cls, redis_client, uuid):
        """Redisからインスタンス化する.

        :param RedisClient redis_client: Redisクライアント
        :param str uuid: Device UUID
        :return: Deviceオブジェクト
        :rtype: Optional[Device]
        """
        key = 'device_{}'.format(uuid)
        if key not in redis_client.keys():
            return None
        if redis_client.type(key) != 'hash':
            return None
        fields = redis_client.hgetall(key)  # type: Dict[str, Any]
        return Device(**fields)

    @classmethod
    def init_all_items_from_redis(cls, redis_client):
        """Redisから全てのDeviceオブジェクトをインスタンス化する.

        :param RedisClient redis_client: Redisクライアント
        :return: 全てのDeviceオブジェクト
        :rtype: List[Device]
        """
        # TODO: UUIDのマッチ部分
        keys = [key for key in redis_client.keys() if re.match(r'^device_[0-9a-fA-F-]+', key)]
        instances = []
        for key in keys:
            if redis_client.type(key) == 'hash':
                fields = redis_client.hgetall(key)  # type: Dict[str, Any]
                instances.append(Device(**fields))
        return instances

    def register_to_redis(self, redis_client):
        """Redisに登録する.

        :param RedisClient redis_client: Redisクライアント
        """
        mapping = {
            'uuid': self.uuid,
            'display_name': self.display_name,
            'schema_uuid': self.schema_uuid,
        }
        for i, prop in enumerate(self.properties, start=1):
            mapping['property{}'.format(i)] = prop.name
            mapping['value{}'.format(i)] = prop.value

        key = 'device_{}'.format(self.uuid)
        redis_client.hmset(key, mapping)

    def unregister_from_redis(self, redis_client):
        """Redisから削除する.

        :param RedisClient redis_client: Redisクライアント
        """
        key = 'device_{}'.format(self.uuid)
        redis_client.delete(key)

    def update_in_redis(self, redis_client):
        """Redis上のデータを更新する.

        :param RedisClient redis_client: Redisクライアント
        """
        key = 'device_{}'.format(self.uuid)
        hkeys = [hkey for hkey in redis_client.hkeys(key)
                 if hkey.startswith('property') or hkey.startswith('value')]
        redis_client.hdel(key, *hkeys)
        self.register_to_redis(redis_client)
