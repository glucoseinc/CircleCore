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


class ConfigError(Exception):
    pass


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

    def matched_device(self, device_uuid):
        """デバイスリストから表示名がマッチするものを取得する.

        :param str device_uuid: 取得するデバイスのUUID
        :return: マッチしたスキーマ
        :rtype: Optional[Device]
        """
        devices = [device for device in self.devices if device.uuid == device_uuid]
        return devices[0] if len(devices) != 0 else None

    @property
    def readable(self):
        """Configが読み込み可能か.

        :return: Configが読み込み可能か
        :rtype: bool
        """
        return False

    @property
    def writable(self):
        """Configが書き込み可能か.

        :return: Configが書き込み可能か
        :rtype: bool
        """
        return False

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

        raise ConfigError('No matching URL scheme.')


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

        # TODO: UUIDのマッチ部分
        schema_dicts = [dict(parser.items(section)) for section in parser.sections()
                        if re.match(r'^schema_[0-9a-fA-F-]+', section)]
        schemas = [Schema(**schema_dict) for schema_dict in schema_dicts]

        device_dicts = [dict(parser.items(section)) for section in parser.sections()
                        if re.match(r'^device_[0-9a-fA-F-]+', section)]
        devices = [Device(**device_dict) for device_dict in device_dicts]

        return ConfigIniFile(schemas, devices)

    @property
    def readable(self):
        """Configが書き込み可能か.

        :return: Configが書き込み可能か
        :rtype: bool
        """
        return True


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
            raise ConfigError('Cannot connect to Redis server.')

        schemas = Schema.init_all_items_from_redis(redis_client)
        devices = Device.init_all_items_from_redis(redis_client)

        return ConfigRedis(schemas, devices, redis_client)

    @property
    def readable(self):
        """Configが書き込み可能か.

        :return: Configが書き込み可能か
        :rtype: bool
        """
        return True

    @property
    def writable(self):
        """Configが書き込み可能か.

        :return: Configが書き込み可能か
        :rtype: bool
        """
        return True
