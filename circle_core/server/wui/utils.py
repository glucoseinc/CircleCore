# -*- coding:utf-8 -*-

# system module
import re

# community module
from flask import current_app, request
from flask.json import _dump_arg_defaults, _json, JSONEncoder as BaseJSONEncoder, text_type
from six import PY3

# project module
from circle_core.models.metadata import MetadataIniFile, MetadataRedis

if PY3:
    from typing import Any, Dict, Union


class JSONEncoder(BaseJSONEncoder):
    pass


def dumps(obj, **kwargs):
    _dump_arg_defaults(kwargs)
    encoding = kwargs.pop('encoding', None)
    kwargs['cls'] = JSONEncoder
    rv = _json.dumps(obj, **kwargs)
    if encoding is not None and isinstance(rv, text_type):
        rv = rv.encode(encoding)
    return rv


def api_jsonify(*args, **kwargs):
    """flask.json.jsonify"""
    indent = None
    _status = kwargs.pop('_status', None)
    if current_app.config['JSONIFY_PRETTYPRINT_REGULAR'] \
       and not request.is_xhr:
        indent = 2
    return current_app.response_class(
        dumps(dict(*args, **kwargs), indent=indent),
        status=_status,
        mimetype='application/json; charset=utf-8')


def get_metadata():
    """Metadataを返す.

    :return:Metadata
    :rtype: Union[MetadataIniFile, MetadataRedis]
    """
    metadata = current_app.config.get('METADATA')
    if metadata is None:
        raise Exception  # TODO: 適切な例外投げる
    return metadata


def convert_dict_key_camel_case(obj):
    """辞書のkeyをsnake caseからcamel caseに変換する.

    :param Union[Dict[str, Any], List, Any] obj: 辞書/リスト/その他
    :return: 変換後辞書
    :rtype: Dict[str, Any]
    """
    def to_camel(value):
        if value is None:
            return None

        words = value.lower().split('_')
        words = [word.capitalize() if i != 0 else word for i, word in enumerate(words)]

        return ''.join(words)

    if isinstance(obj, dict):
        return {to_camel(key): convert_dict_key_camel_case(val) for key, val in obj.items()}

    if isinstance(obj, list):
        return [convert_dict_key_camel_case(item) for item in obj]

    return obj


def convert_dict_key_snake_case(obj):
    """辞書のkeyをcamel caseからsnake caseに変換する.

    :param Union[Dict[str, Any], List, Any] obj: 辞書/リスト/その他
    :return: 変換後辞書
    :rtype: Dict[str, Any]
    """
    def to_snake(value):
        if value is None or value == '':
            return value

        ret = re.sub(r'([\s|A-Z])', "_\\1", value)
        ret = re.sub(r'([\s])', "", ret)
        ret = re.sub(r'^_', "", ret)
        ret = ret.lower()

        return ret

    if isinstance(obj, dict):
        return {to_snake(key): convert_dict_key_snake_case(val) for key, val in obj.items()}

    if isinstance(obj, list):
        return [convert_dict_key_snake_case(item) for item in obj]

    return obj


def oauth_require_user_scope(f):
    """user情報の読み書きが行えるScope"""
    from .authorize import oauth
    return oauth.require_oauth('user')(f)


def oauth_require_read_schema_scope(f):
    """(User以外の）メタデータを読むだけのScope"""
    from .authorize import oauth
    return oauth.require_oauth('schema+r', 'schema+rw')(f)


def oauth_require_write_schema_scope(f):
    """(User以外の）メタデータを読み書きするためのScope"""
    from .authorize import oauth
    return oauth.require_oauth('schema+rw')(f)
