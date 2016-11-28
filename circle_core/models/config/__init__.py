# -*- coding: utf-8 -*-

# community module
from six import PY2

# project module
from .config_base import Config, ConfigError
from .config_inifile import ConfigIniFile
from .config_redis import ConfigRedis

if PY2:
    from urlparse import urlparse
else:
    from urllib.parse import urlparse


def parse_url_scheme(url_scheme):
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
