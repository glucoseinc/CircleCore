# -*- coding: utf-8 -*-

# system module
import os

# community module
from six.moves import configparser
from six.moves.urllib.parse import urlparse

# project module
from .base import MetadataError, MetadataReader
from ..module import Module
from ..schema import Schema


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
        if not os.path.exists(ini_file_path):
            raise MetadataError('INI file "{}" not found.'.format(ini_file_path))

        return MetadataIniFile(ini_file_path)

    @property
    def schemas(self):
        parser = configparser.ConfigParser()
        parser.read(self.ini_file_path)
        schema_dicts = [dict(parser.items(section)) for section in parser.sections() if Schema.is_key_matched(section)]
        return [Schema(**schema_dict) for schema_dict in schema_dicts]

    @property
    def modules(self):
        parser = configparser.ConfigParser()
        parser.read(self.ini_file_path)
        module_dicts = [dict(parser.items(section)) for section in parser.sections() if Module.is_key_matched(section)]
        return [Module(**module_dict) for module_dict in module_dicts]
