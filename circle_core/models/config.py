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
    from typing import List


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


class Config(object):
    """Configオブジェクト.

    :param ConfigType _type: Configタイプ
    :param List[Schema] schemas: スキーマ
    :param List[Device] devices: デバイス
    """

    def __init__(self, config_type, schemas, devices):
        """init.

        :param ConfigType config_type: Configタイプ
        :param List[Schema] schemas: スキーマ
        :param List[Device] devices: デバイス
        """
        self._type = config_type
        self.schemas = schemas
        self.devices = devices

    @property
    def type(self):
        """Configタイプ.

        :return: Configタイプ
        :rtype: int
        """
        return self._type.type

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

        return Config(ConfigType(ConfigType.redis), schemas, devices)
