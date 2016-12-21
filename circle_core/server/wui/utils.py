# -*- coding:utf-8 -*-

# community module
from flask import current_app, request
from flask.json import _dump_arg_defaults, _json, JSONEncoder as BaseJSONEncoder, text_type
from six import PY3

# project module
from circle_core.models.metadata import MetadataIniFile, MetadataRedis

if PY3:
    from typing import Union


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
    if current_app.config['JSONIFY_PRETTYPRINT_REGULAR'] \
       and not request.is_xhr:
        indent = 2
    return current_app.response_class(
        dumps(dict(*args, **kwargs), indent=indent),
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
