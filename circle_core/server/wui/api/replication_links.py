# -*- coding: utf-8 -*-

"""共有リンク関連APIの実装."""

# community module
from flask import abort, request

# project module
from circle_core.cli.utils import generate_uuid
from circle_core.models import ReplicationLink
from .api import api
from .utils import respond_failure
from ..utils import (
    api_jsonify, api_response_failure, convert_dict_key_camel_case, convert_dict_key_snake_case, get_metadata,
    oauth_require_read_schema_scope, oauth_require_write_schema_scope
)


@api.route('/replicas/', methods=['GET', 'POST'])
def api_replicas():
    if request.method == 'GET':
        return _get_replicas()
    if request.method == 'POST':
        return _post_replicas()
    abort(405)


@oauth_require_read_schema_scope
def _get_replicas():
    metadata = get_metadata()

    response = {
        'cc_infos': [cc_info.to_json() for cc_info in metadata.cc_infos],
        'modules': [metadata.denormalize_json_module(module.uuid) for module in metadata.modules],  # 必要な分だけに絞るべきか？
        'replication_links': [replication_link.to_json() for replication_link in metadata.replication_links]
    }
    return api_jsonify(**convert_dict_key_camel_case(response))


@oauth_require_write_schema_scope
def _post_replicas():
    dic = convert_dict_key_snake_case(request.json)
    response = {}  # TODO: response形式の統一
    try:
        display_name = dic['display_name']
        cc_info_uuids = ['00000000-0000-0000-0000-000000000000']  # TODO: Dummy
#        cc_info_uuids = dic['cc_infos']
        message_box_uuids = dic['message_boxes']
        memo = dic['memo']
        if len(memo) == 0:
            memo = None
    except KeyError:
        return api_response_failure('key error')

    metadata = get_metadata()
    replication_link_uuid = generate_uuid(
        existing=[replication_link.uuid for replication_link in metadata.replication_links]
    )
    replication_link = ReplicationLink(replication_link_uuid, cc_info_uuids, message_box_uuids, display_name, memo)
    metadata.register_replication_link(replication_link)
    response['result'] = 'success'
    response['replication_link'] = replication_link.to_json()
    return api_jsonify(**convert_dict_key_camel_case(response))


@api.route('/replicas/<uuid:replication_link_uuid>', methods=['GET', 'DELETE'])
def api_replica(replication_link_uuid):
    if request.method == 'GET':
        return _get_replica(replication_link_uuid)
    elif request.method == 'DELETE':
        return _delete_replica(replication_link_uuid)
    abort(405)


@oauth_require_read_schema_scope
def _get_replica(replication_link_uuid):
    metadata = get_metadata()

    response = {
        'replication_link': metadata.find_replication_link(replication_link_uuid).to_json()
    }
    return api_jsonify(**convert_dict_key_camel_case(response))


@oauth_require_write_schema_scope
def _delete_replica(replication_link_uuid):
    metadata = get_metadata()
    replication_link = metadata.find_replication_link(replication_link_uuid)
    if replication_link is None:
        return respond_failure('Replication Link not found.', _status=404)

    metadata.unregister_replication_link(replication_link)
    response = {
        'replication_link': replication_link.to_json()
    }
    return api_jsonify(**convert_dict_key_camel_case(response))
