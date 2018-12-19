# -*- coding: utf-8 -*-
"""スキーマ関連APIの実装."""

# community module
from flask import abort, request

# project module
from circle_core.constants import CRDataType
from circle_core.models import MetaDataSession, Schema

from .api import api
from .utils import respond_failure, respond_success
from ..utils import (oauth_require_read_schema_scope, oauth_require_write_schema_scope)


@api.route('/schemas/', methods=['GET', 'POST'])
def api_schemas():
    """全てのSchemaのCRUD."""
    if request.method == 'GET':
        return _get_schemas()
    if request.method == 'POST':
        return _post_schemas()
    abort(405)


@oauth_require_read_schema_scope
def _get_schemas():
    """全てのSchemaの情報を取得する.

    :return: 全てのSchemaの情報
    :rtype: Response
    """
    return respond_success(schemas=[schema.to_json(with_modules=True) for schema in Schema.query])


@oauth_require_write_schema_scope
def _post_schemas():
    """Schemaを作成する.

    :return: 作成したSchemaの情報
    :rtype: Response
    """
    with MetaDataSession.begin():
        schema = Schema.create()
        schema.update_from_json(request.json)
        MetaDataSession.add(schema)

    return respond_success(schema=schema.to_json(with_modules=True))


@api.route('/schemas/<schema_uuid>', methods=['GET', 'DELETE'])
def api_schema(schema_uuid):
    """単一のSchemaのCRUD."""
    # TODO: Sub Fuctionに渡す前にSchemaの実体を取得する
    if request.method == 'GET':
        return _get_schema(schema_uuid)
    if request.method == 'DELETE':
        return _delete_schema(schema_uuid)
    # SchemaのUpdateはなし
    abort(405)


@oauth_require_read_schema_scope
def _get_schema(schema_uuid):
    """Schemaの情報を取得する.

    :param str schema_uuid: 取得するSchemaのUUID
    :return: Schemaの情報
    :rtype: Response
    """
    schema = Schema.query.get(schema_uuid)
    if not schema:
        return respond_failure('not found', _status=404)

    return respond_success(schema=schema.to_json(with_modules=True))


@oauth_require_write_schema_scope
def _delete_schema(schema_uuid):
    """Schemaを削除する.

    :param str schema_uuid: 削除するSchemaのUUID
    :return: Schemaの情報
    :rtype: Response
    """
    schema = Schema.query.get(schema_uuid)
    if not schema:
        return respond_failure('not found', _status=404)

    if len(schema.message_boxes) > 0:
        reason = 'message box {uuids} {verb} attached'.format(
            uuids=', '.join([str(box.uuid) for box in schema.message_boxes]),
            verb='is' if len(schema.message_boxes) == 1 else 'are'
        )
        return respond_failure(reason, _status=400)

    with MetaDataSession.begin():
        MetaDataSession.delete(schema)

    return respond_success(schema={'uuid': schema_uuid})


@api.route('/schemas/propertytypes')
@oauth_require_read_schema_scope
def api_get_property_types():
    """全てのSchemaProperty Typeを取得する."""
    property_types = [{'name': data_type.value} for data_type in CRDataType]
    return respond_success(schemaPropertyTypes=property_types)
