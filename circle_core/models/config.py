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


class Config(object):
    """Configオブジェクト.

    :param str stringified_type: Configタイプ(str)
    :param List[Schema] schemas: スキーマリスト
    :param List[Device] devices: デバイスリスト
    """

    stringified_type = 'nothing'

    def __init__(self, schemas, devices):
        """init.

        :param List[Schema] schemas: スキーマリスト
        :param List[Device] devices: デバイスリスト
        """
        self.schemas = schemas
        self.devices = devices

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
    def parse(cls, url_scheme):
        """URLスキームからConfigオブジェクトを生成する.

        :param str url_scheme: URLスキーム
        :return: Configオブジェクト
        :rtype: Config
        """
        parsed_url = urlparse(url_scheme)
        if parsed_url.scheme == 'file':
            return ConfigIniFile.parse_url_scheme(url_scheme)
        elif parsed_url.scheme == 'redis':
            return ConfigRedis.parse_url_scheme(url_scheme)

        return Config([], [])


class ConfigIniFile(Config):
    """ConfigIniFileオブジェクト.

    """

    stringified_type = 'INI File'

    @classmethod
    def parse_url_scheme(cls, url_scheme):
        """iniファイルからConfigオブジェクトを生成する.

        :param str url_scheme: URLスキーム
        :return: ConfigIniFileオブジェクト
        :rtype: ConfigIniFile
        """
        ini_file_path = urlparse(url_scheme).path
        parser = configparser.ConfigParser()
        parser.read(ini_file_path)

        schema_dicts = [dict(parser.items(section)) for section in parser.sections()
                        if re.match(r'^schema\d+', section)]
        schemas = [Schema(**schema_dict) for schema_dict in schema_dicts]

        device_dicts = [dict(parser.items(section)) for section in parser.sections()
                        if re.match(r'^device\d+', section)]
        devices = [Device(**device_dict) for device_dict in device_dicts]

        return ConfigIniFile(schemas, devices)


class ConfigRedis(Config):
    """ConfigRedisオブジェクト.

    :param RedisClient redis_client: Redisクライアント
    """

    stringified_type = 'Redis'

    def __init__(self, schemas, devices, redis_client):
        """init.

        :param List[Schema] schemas: スキーマリスト
        :param List[Device] devices: デバイスリスト
        :param RedisClient redis_client: Redisクライアント
        """
        super(ConfigRedis, self).__init__(schemas, devices)
        self.redis_client = redis_client

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
        except redis.ConnectionError:
            # TODO: 適切な例外処理
            return ConfigRedis([], [], None)

        schemas = Schema.init_all_items_from_redis(redis_client)
        devices = Device.init_all_items_from_redis(redis_client)

        return ConfigRedis(schemas, devices, redis_client)
