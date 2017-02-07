# -*- coding: utf-8 -*-

"""CircleCoreInfo関連APIの実装."""

# community module
from flask import abort, request

# project module
from circle_core.models import CcInfo, MetaDataSession
from .api import api
from .utils import respond_failure
from ..utils import (
    api_jsonify,
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
    response = {
        'ccInfos': [cc_info.to_json() for cc_info in CcInfo.query]
    }
    return api_jsonify(**response)


@oauth_require_read_schema_scope
def _post_cores():
    # TODO: implement
    response = {}
    return api_jsonify(**response)


@api.route('/cores/myself', methods=['GET'])
def api_core_myself():
    if request.method == 'GET':
        return _get_core_myself()
    abort(405)


@oauth_require_read_schema_scope
def _get_core_myself():
    response = {
        'ccInfo': CcInfo.query.filter_by(myself=True).one().to_json()
    }
    return api_jsonify(**response)


@api.route('/cores/<uuid:cc_info_uuid>', methods=['GET', 'PUT'])
def api_core(cc_info_uuid):
    cc_info = CcInfo.query.get(cc_info_uuid)
    if not cc_info:
        return respond_failure('not found', _status=404)

    if request.method == 'GET':
        return _get_core(cc_info)
    if request.method == 'PUT':
        return _put_core(cc_info)
    abort(405)


@oauth_require_read_schema_scope
def _get_core(cc_info):
    return api_jsonify(ccInfo=cc_info.to_json())


@oauth_require_write_schema_scope
def _put_core(cc_info):
    with MetaDataSession.begin():
        cc_info.update_from_json(request.json)
        MetaDataSession.add(cc_info)

    # TODO: response形式の統一
    return api_jsonify(result='success', ccInfo=cc_info.to_json())
