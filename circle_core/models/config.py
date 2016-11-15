#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from urlparse import urlparse
except ImportError:
    from urllib.parse import urlparse

try:
    import ConfigParser as configparser
except ImportError:
    import configparser

from .device import Device
from .schema import Schema


class Config(object):
    def __init__(self, schemas, devices):
        # type: (list, list) -> None
        self.schemas = schemas
        self.devices = devices

    # TODO: schemaとconfigのstrを整形して返す
    def __str__(self):
        # type: () -> str
        return 'config_string'

    @classmethod
    def parse(cls, url_string):
        # type: (str) -> Config
        schemas = []
        devices = []

        parsed_url = urlparse(url_string)
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
