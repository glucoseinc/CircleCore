# -*- coding: utf-8 -*-

"""CircleCoreInfo関連APIの実装."""

# community module
from flask import abort, request

# project module
from circle_core.models import CcInfo
from .api import api
from ..utils import (
    api_jsonify, convert_dict_key_camel_case, convert_dict_key_snake_case, get_metadata,
    oauth_require_read_schema_scope, oauth_require_write_schema_scope
)


@api.route('/cores/', methods=['GET', 'POST'])
def api_cores():
    if request.method == 'GET':
        return _get_cores()
    if request.method == 'POST':
        return _post_cores()
    abort(405)


@oauth_require_read_schema_scope
def _get_cores():
    metadata = get_metadata()

    response = {
        'cc_infos': [cc_info.to_json() for cc_info in metadata.cc_infos]
    }
    return api_jsonify(**convert_dict_key_camel_case(response))


@oauth_require_read_schema_scope
def _post_cores():
    # TODO: implement
    response = {}
    return api_jsonify(**convert_dict_key_camel_case(response))


@api.route('/cores/myself', methods=['GET', 'PUT'])
def api_core_myself():
    if request.method == 'GET':
        return _get_core_myself()
    if request.method == 'PUT':
        return _put_core_myself()
    abort(405)


@oauth_require_read_schema_scope
def _get_core_myself():
    metadata = get_metadata()

    response = {
        'cc_info': metadata.find_own_cc_info().to_json()
    }
    return api_jsonify(**convert_dict_key_camel_case(response))


@oauth_require_write_schema_scope
def _put_core_myself():
    response = {}  # TODO: response形式の統一

    metadata = get_metadata()
    dic = convert_dict_key_snake_case(request.json)
    own_cc_info = CcInfo(**dic)

    metadata.update_cc_info(own_cc_info)

    response['result'] = 'success'
    response['detail'] = {}
    return api_jsonify(**convert_dict_key_camel_case(response))
