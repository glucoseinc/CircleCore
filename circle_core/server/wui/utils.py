# -*- coding:utf-8 -*-
from flask import current_app, request
from flask.json import _dump_arg_defaults, _json, JSONEncoder as BaseJSONEncoder, text_type


__all__ = ('api_jsonify',)


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
