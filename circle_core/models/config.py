#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Config Model."""

# system module
import re

# community module
import redis
from six import PY2

# project module
from .device import Device
from .redis_client import RedisClient
from .schema import Schema

if PY2:
    from urlparse import urlparse
    import ConfigParser as configparser
else:
    from urllib.parse import urlparse
    import configparser
    from typing import List, Optional


class ConfigType(object):
    """ConfigTypeオブジェクト.

    :param int type: Configタイプ
    """

    (
        nothing,
        redis,
        ini_file,
    ) = range(3)

    def __init__(self, config_type):
        """init.

        :param int config_type: Configタイプ
        """
        self.type = config_type

    def __str__(self):
        """str.

        :return: str
        :rtype: str
        """
        if self.type == ConfigType.nothing:
            return 'Nothing'
        if self.type == ConfigType.redis:
            return 'Redis'
        if self.type == ConfigType.ini_file:
            return 'INI File'
        return 'Nothing'


class Config(object):
    """Configオブジェクト.

    :param ConfigType _type: Configタイプ
    :param List[Schema] schemas: スキーマリスト
    :param List[Device] devices: デバイスリスト
    :param Optional[RedisClient] redis_client: Redisクライアント
    """

    def __init__(self, config_type, schemas, devices, redis_client=None):
        """init.

        :param ConfigType config_type: Configタイプ
        :param List[Schema] schemas: スキーマリスト
        :param List[Device] devices: デバイスリスト
        :param Optional[RedisClient] redis_client: Redisクライアント
        """
        self._type = config_type
        self.schemas = schemas
        self.devices = devices
        self.redis_client = redis_client

    @property
    def type(self):
        """Configタイプ(enum).

        :return: Configタイプ
        :rtype: int
        """
        return self._type.type

    @property
    def stringified_type(self):
        """Configタイプ(str).

        :return: Configタイプ
        :rtype: str
        """
        return str(self._type)

    def matched_schema(self, schema_uuid):
        """スキーマリストからUUIDがマッチするものを取得する.

        :param str schema_uuid: 取得するスキーマのUUID
        :return: マッチしたスキーマ
        :rtype: Optional[Schema]
        """
        schemas = [schema for schema in self.schemas if schema.uuid == schema_uuid]
        return schemas[0] if len(schemas) != 0 else None

    def matched_device(self, device_name):
        """デバイスリストから表示名がマッチするものを取得する.

        :param str device_name: 取得するデバイスの表示名
        :return: マッチしたスキーマ
        :rtype: Optional[Device]
        """
        devices = [device for device in self.devices if device.display_name == device_name]
        return devices[0] if len(devices) != 0 else None

    @classmethod
    def parse(cls, url_schema):
        """URLスキームからConfigオブジェクトを生成する.

        :param str url_schema: URLスキーム
        :return: Configオブジェクト
        :rtype: Config
        """
        parsed_url = urlparse(url_schema)
        if parsed_url.scheme == 'file':
            return Config._parse_ini(parsed_url.path)
        elif parsed_url.scheme == 'redis':
            return Config._parse_redis(url_schema)

        return Config(ConfigType(ConfigType.nothing), [], [])

    @classmethod
    def _parse_ini(cls, ini_file_path):
        """iniファイルからConfigオブジェクトを生成する.

        :param str ini_file_path: iniファイルのパス
        :return: Configオブジェクト
        :rtype: Config
        """
        parser = configparser.ConfigParser()
        parser.read(ini_file_path)

        schema_dicts = [dict(parser.items(section)) for section in parser.sections()
                        if re.match(r'^schema\d+', section)]
        schemas = [Schema(**schema_dict) for schema_dict in schema_dicts]

        device_dicts = [dict(parser.items(section)) for section in parser.sections()
                        if re.match(r'^device\d+', section)]
        devices = [Device(**device_dict) for device_dict in device_dicts]

        return Config(ConfigType(ConfigType.ini_file), schemas, devices)

    @classmethod
    def _parse_redis(cls, url_schema):
        """redisからConfigオブジェクトを生成する.

        :param str url_schema: URLスキーム
        :return: Configオブジェクト
        :rtype: Config
        """
        try:
            redis_client = RedisClient.from_url(url_schema)
            redis_client.ping()
        except redis.ConnectionError:
            # TODO: 適切な例外処理
            return Config(ConfigType(ConfigType.redis), [], [])

        schemas = Schema.init_all_items_from_redis(redis_client)
        devices = Device.init_all_items_from_redis(redis_client)

        return Config(ConfigType(ConfigType.redis), schemas, devices, redis_client=redis_client)
