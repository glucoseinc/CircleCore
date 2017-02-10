# -*- coding: utf-8 -*-

"""共有リンク関連APIの実装."""

# community module
from flask import abort, request

# project module
from circle_core.models import ReplicationLink
from .api import api
from .utils import respond_failure, respond_success
from ..utils import (
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
    return respond_success(
        ccInfos=[cc_info.to_json() for cc_info in metadata.cc_infos],
        modules=[metadata.denormalize_json_module(module.uuid) for module in metadata.modules],  # 必要な分だけに絞るべきか？
        replicationLinks=[replication_link.to_json() for replication_link in metadata.replication_links]
    )


@oauth_require_write_schema_scope
def _post_replicas():
    # dic = convert_dict_key_snake_case(request.json)
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
        return respond_failure('key error')

    replication_link_uuid = generate_uuid(
        existing=[replication_link.uuid for replication_link in metadata.replication_links]
    )
    replication_link = ReplicationLink(replication_link_uuid, cc_info_uuids, message_box_uuids, display_name, memo)
    metadata.register_replication_link(replication_link)
    response['result'] = 'success'
    response['replicationLink'] = replication_link.to_json()
    return api_jsonify(**response)


@api.route('/replicas/<uuid:replication_link_uuid>', methods=['GET', 'DELETE'])
def api_replica(replication_link_uuid):
    replication_link = ReplicationLink.query.get(replication_link_uuid)
    if not replication_link:
        return respond_failure('Replication Link not found.', _status=404)

    if request.method == 'GET':
        return _get_replica(replication_link)
    elif request.method == 'DELETE':
        return _delete_replica(replication_link)
    abort(405)


@oauth_require_read_schema_scope
def _get_replica(replication_link):
    return respond_success(
        replicationLink=replication_link.to_json()
    )


@oauth_require_write_schema_scope
def _delete_replica(replication_link):
    with MetaDataSession.begin():
        MetaDataSession.delete(replication_link)

    return respond_success(
        replicationLink=replication_link.to_json()
    )
