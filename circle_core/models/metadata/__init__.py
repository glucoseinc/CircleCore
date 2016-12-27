# -*- coding: utf-8 -*-

# community module
from click import get_current_context
from six import PY3
from six.moves.urllib.parse import urlparse

# project module
from .base import MetadataBase as Metadata, MetadataError
from .inifile import MetadataIniFile
from .redis import MetadataRedis

if PY3:
    from typing import Union


def parse_url_scheme(url_scheme):
    """URLスキームからMetadataオブジェクトを生成する.

    :param str url_scheme: URLスキーム
    :return: Metadataオブジェクト
    :rtype: Union[MetadataIniFile, MetadataRedis]
    """
    parsed_url = urlparse(url_scheme)
    if parsed_url.scheme == 'file':
        return MetadataIniFile.parse_url_scheme(url_scheme)
    elif parsed_url.scheme == 'redis':
        return MetadataRedis.parse_url_scheme(url_scheme)

    raise MetadataError('No matching URL scheme.')


def metadata():
    """metadata getter."""
    try:
        return get_current_context().obj.metadata
    except RuntimeError:
        # raise from 使いたいがPython2がサポートしていない
        raise NotImplementedError('Click context not found. You must set some mock metadata in the tests.')
