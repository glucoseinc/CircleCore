# -*- coding: utf-8 -*-
"""共有マスター関連APIの実装."""

# community module
from flask import abort, request
import sqlalchemy.exc

# project module
from circle_core.models import MetaDataSession, ReplicationMaster
from .api import api
from .utils import respond_failure, respond_success
from ..utils import (oauth_require_read_schema_scope, oauth_require_write_schema_scope)


@api.route('/replication_masters/', methods=['GET', 'POST'])
def api_repliction_masters():
    """全てのReplicationMasterのCRUD."""
    if request.method == 'GET':
        return _get_replication_masters()
    elif request.method == 'POST':
        return _post_replication_masters()
    abort(405)


@oauth_require_read_schema_scope
def _get_replication_masters():
    """全てのReplicationMasterの情報を取得する.

    :return: 全てのReplicationMasterの情報
    :rtype: Response
    """
    # TODO: earger loading
    replication_masters = [obj.to_json() for obj in ReplicationMaster.query]

    return respond_success(replicationMasters=replication_masters)


@oauth_require_write_schema_scope
def _post_replication_masters():
    """ReplicationMasterを作成する.

    :return: 作成したReplicationMasterの情報
    :rtype: Response
    """
    data = request.json
    try:
        with MetaDataSession.begin():
            replication_master = ReplicationMaster(endpoint_url=data['endpointUrl'],)

            MetaDataSession.add(replication_master)
    except sqlalchemy.exc.IntegrityError:
        return respond_failure('このURLは既に登録されています')

    return respond_success(replicationMaster=replication_master.to_json())


@api.route('/replication_masters/<int:replication_master_id>', methods=['GET', 'DELETE'])
def api_replication_master(replication_master_id):
    """単一のReplicationMasterのCRUD."""
    repmaster = ReplicationMaster.query.get(replication_master_id)
    if not repmaster:
        return respond_failure('Replication Master not found.', _status=404)

    if request.method == 'GET':
        return _get_replication_master(repmaster)
    elif request.method == 'DELETE':
        return _delete_replication_master(repmaster)
    abort(405)


@oauth_require_read_schema_scope
def _get_replication_master(replication_master):
    """ReplicationMasterの情報を取得する.

    :param ReplicationMaster replication_master: 取得するReplicationMaster
    :return: ReplicationMasterの情報
    :rtype: Response
    """
    return respond_success(replicationMaster=replication_master.to_json())


@oauth_require_write_schema_scope
def _delete_replication_master(replication_master):
    """ReplicationMasterを削除する.

    :param ReplicationMaster replication_master: 削除するReplicationMaster
    :return: ReplicationMasterの情報
    :rtype: Response
    """
    with MetaDataSession.begin():
        MetaDataSession.delete(replication_master)

    return respond_success(replicationMaster=replication_master.to_json())
