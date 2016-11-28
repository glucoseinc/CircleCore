# -*- coding: utf-8 -*-

# system module
import re

# community module
from six import PY2

# project module
from .config_base import Config, ConfigError
from ..device import Device
from ..schema import Schema

if PY2:
    from urlparse import urlparse
    import ConfigParser as configparser
else:
    from urllib.parse import urlparse
    import configparser


class ConfigIniFile(Config):
    """ConfigIniFileオブジェクト.

    :param str ini_file_path: INIファイルパス
    """

    stringified_type = 'INI File'

    def __init__(self, ini_file_path):
        """init.

        :param str ini_file_path: INIファイルパス
        """
        super(ConfigIniFile, self).__init__()
        self.ini_file_path = ini_file_path

        self._instantiate_all_schemas()
        self._instantiate_all_devices()

    @classmethod
    def parse_url_scheme(cls, url_scheme):
        """iniファイルからConfigオブジェクトを生成する.

        :param str url_scheme: URLスキーム
        :return: ConfigIniFileオブジェクト
        :rtype: ConfigIniFile
        """
        ini_file_path = urlparse(url_scheme).path
        return ConfigIniFile(ini_file_path)

    @property
    def readable(self):
        return True

    @property
    def writable(self):
        return False

    def _instantiate_all_schemas(self):
        self.schemas = []
        # TODO: UUIDのマッチ部分
        parser = configparser.ConfigParser()
        parser.read(self.ini_file_path)
        schema_dicts = [dict(parser.items(section)) for section in parser.sections()
                        if re.match(r'^schema_[0-9a-fA-F-]+', section)]
        self.schemas = [Schema(**schema_dict) for schema_dict in schema_dicts]

    def register_schema(self, schema):
        raise ConfigError('Cannot register schema because read only storage.')

    def unregister_schema(self, schema):
        raise ConfigError('Cannot unregister schema because read only storage.')

    def _instantiate_all_devices(self):
        self.devices = []
        # TODO: UUIDのマッチ部分
        parser = configparser.ConfigParser()
        parser.read(self.ini_file_path)
        device_dicts = [dict(parser.items(section)) for section in parser.sections()
                        if re.match(r'^device_[0-9a-fA-F-]+', section)]
        self.devices = [Device(**device_dict) for device_dict in device_dicts]

    def register_device(self, device):
        raise ConfigError('Cannot register device because read only storage.')

    def unregister_device(self, device):
        raise ConfigError('Cannot unregister device because read only storage.')

    def update_device(self, device):
        raise ConfigError('Cannot update device because read only storage.')
