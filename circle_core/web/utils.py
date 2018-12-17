# -*- coding:utf-8 -*-
"""WebUI Utilities."""

from typing import TYPE_CHECKING

# community module
from flask import current_app, request
from flask.json import JSONEncoder as BaseJSONEncoder, _dump_arg_defaults, _json, text_type

# project module
from circle_core.constants import CRScope

# type annotation
if TYPE_CHECKING:
    from typing import Any, Callable


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
    """flask.json.jsonify."""
    indent = None
    _status = kwargs.pop('_status', None)
    if current_app.config['JSONIFY_PRETTYPRINT_REGULAR'] \
       and not request.is_xhr:
        indent = 2
    return current_app.response_class(
        dumps(dict(*args, **kwargs), indent=indent), status=_status, mimetype='application/json; charset=utf-8'
    )


def oauth_require_read_users_scope(f: 'Callable[..., Any]'):
    """user情報の読み込みが行えるScopeデコレータ.

    :param Callable f: Function
    """
    from .authorize import oauth
    return oauth.require_oauth(CRScope.USER_R.value, CRScope.USER_RW.value)(f)


def oauth_require_write_users_scope(f: 'Callable[..., Any]'):
    """user情報の変更が行えるScopeデコレータ.

    :param Callable f: Function
    """
    from .authorize import oauth
    return oauth.require_oauth(CRScope.USER_RW.value)(f)


def oauth_require_read_schema_scope(f: 'Callable[..., Any]'):
    """(User以外の）メタデータを読むだけのScopeデコレータ.

    :param Callable f: Function
    """
    from .authorize import oauth
    return oauth.require_oauth(CRScope.SCHEMA_R.value, CRScope.SCHEMA_RW.value)(f)


def oauth_require_write_schema_scope(f: 'Callable[..., Any]'):
    """(User以外の）メタデータを読み書きするためのScopeデコレータ.

    :param Callable f: Function
    """
    from .authorize import oauth
    return oauth.require_oauth(CRScope.SCHEMA_RW.value)(f)
