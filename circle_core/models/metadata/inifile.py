# -*- coding: utf-8 -*-

# community module
from six import PY2

# project module
from .base import MetadataReader
from ..device import Device
from ..schema import Schema

if PY2:
    from urlparse import urlparse
    import ConfigParser as configparser
else:
    from urllib.parse import urlparse
    import configparser


class MetadataIniFile(MetadataReader):
    """MetadataIniFileオブジェクト.

    :param str ini_file_path: INIファイルパス
    """

    stringified_type = 'INI File'

    def __init__(self, ini_file_path):
        """init.

        :param str ini_file_path: INIファイルパス
        """
        super(MetadataIniFile, self).__init__()
        self.ini_file_path = ini_file_path

    @classmethod
    def parse_url_scheme(cls, url_scheme):
        ini_file_path = urlparse(url_scheme).path
        return MetadataIniFile(ini_file_path)

    @property
    def schemas(self):
        parser = configparser.ConfigParser()
        parser.read(self.ini_file_path)
        schema_dicts = [dict(parser.items(section)) for section in parser.sections() if Schema.is_key_matched(section)]
        return [Schema(**schema_dict) for schema_dict in schema_dicts]

    @property
    def devices(self):
        parser = configparser.ConfigParser()
        parser.read(self.ini_file_path)
        device_dicts = [dict(parser.items(section)) for section in parser.sections() if Device.is_key_matched(section)]
        return [Device(**device_dict) for device_dict in device_dicts]
