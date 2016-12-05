# -*- coding: utf-8 -*-

# community module
from six import PY2

# project module
from .base import MetadataBase as Metadata, MetadataError
from .inifile import MetadataIniFile
from .redis import MetadataRedis

if PY2:
    from urlparse import urlparse
else:
    from urllib.parse import urlparse


def parse_url_scheme(url_scheme):
    """URLスキームからMetadataオブジェクトを生成する.

    :param str url_scheme: URLスキーム
    :return: Metadataオブジェクト
    :rtype: Metadata
    """
    parsed_url = urlparse(url_scheme)
    if parsed_url.scheme == 'file':
        return MetadataIniFile.parse_url_scheme(url_scheme)
    elif parsed_url.scheme == 'redis':
        return MetadataRedis.parse_url_scheme(url_scheme)

    raise MetadataError('No matching URL scheme.')
