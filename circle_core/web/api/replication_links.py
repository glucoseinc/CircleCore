# -*- coding: utf-8 -*-
"""共有リンク関連APIの実装."""

# community module
from flask import abort, request

# project module
from circle_core.models import MetaDataSession, ReplicationLink
from .api import api
from .utils import respond_failure, respond_success
from ..utils import (oauth_require_read_schema_scope, oauth_require_write_schema_scope)


@api.route('/replicas/', methods=['GET', 'POST'])
def api_replicas():
    """全てのReplicationLinkのCRUD."""
    if request.method == 'GET':
        return _get_replicas()
    elif request.method == 'POST':
        return _post_replicas()
    abort(405)


@oauth_require_read_schema_scope
def _get_replicas():
    """全てのReplicationLinkの情報を取得する.

    :return: 全てのReplicationLinkの情報
    :rtype: Response
    """
    # TODO: earger loading
    replication_links = [
        replication_link.to_json(with_slaves=True, with_boxes=True) for replication_link in ReplicationLink.query
    ]

    return respond_success(replicationLinks=replication_links)


@oauth_require_write_schema_scope
def _post_replicas():
    """ReplicationLinkを作成する.

    :return: 作成したReplicationLinkの情報
    :rtype: Response
    """
    data = request.json
    with MetaDataSession.begin():
        replication_link = ReplicationLink.create(
            data['displayName'],
            data['memo'],
            data['messageBoxes'],
        )
        MetaDataSession.add(replication_link)

    return respond_success(replicationLink=replication_link.to_json())


@api.route('/replicas/<uuid:replication_link_uuid>', methods=['GET', 'DELETE'])
def api_replica(replication_link_uuid):
    """単一のReplicationLinkのCRUD."""
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
    """ReplicationLinkの情報を取得する.

    :param ReplicationLink replication_link: 取得するReplicationLink
    :return: ReplicationLinkの情報
    :rtype: Response
    """
    return respond_success(replicationLink=replication_link.to_json())


@oauth_require_write_schema_scope
def _delete_replica(replication_link):
    """ReplicationLinkを削除する.

    :param ReplicationLink replication_link: 削除するReplicationLink
    :return: ReplicationLinkの情報
    :rtype: Response
    """
    with MetaDataSession.begin():
        MetaDataSession.delete(replication_link)

    return respond_success(replicationLink=replication_link.to_json())
