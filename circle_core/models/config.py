#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Config Model."""

# community module
from six import PY2

# project module
from .device import Device
from .schema import Schema


if PY2:
    from urlparse import urlparse
    import ConfigParser as configparser
else:
    from urllib.parse import urlparse
    import configparser
    from typing import List


class Config(object):
    """Configオブジェクト.

    :param List[Schema] schemas: スキーマ
    :param List[Device] devices: デバイス
    """

    def __init__(self, schemas, devices):
        """init.

        :param List[Schema] schemas: スキーマ
        :param List[Device] devices: デバイス
        """
        self.schemas = schemas
        self.devices = devices

    @classmethod
    def parse(cls, url_schema):
        """URLスキームからConfigオブジェクトを生成する.

        :param str url_schema: URLスキーム
        :return: Configオブジェクト
        :rtype: Config
        """
        schemas = []
        devices = []

        parsed_url = urlparse(url_schema)
        if parsed_url.scheme == 'file':
            ini_file_path = parsed_url.path
            parser = configparser.ConfigParser()
            parser.read(ini_file_path)

            schemas_dict = [dict(parser.items(section)) for section in parser.sections()
                            if section.startswith('schema')]
            for schema_dict in schemas_dict:
                schemas.append(Schema(**schema_dict))

            devices_dict = [dict(parser.items(section)) for section in parser.sections()
                            if section.startswith('device')]
            for device_dict in devices_dict:
                devices.append(Device(**device_dict))

        return Config(schemas, devices)
