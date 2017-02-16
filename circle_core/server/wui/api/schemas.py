# -*- coding: utf-8 -*-

"""スキーマ関連APIの実装."""

# community module
from flask import abort, request
from six import PY3

# project module
# from circle_core.cli.utils import generate_uuid
from circle_core.models import generate_uuid, MetaDataSession, Schema
from .api import api
from .utils import respond_failure, respond_success
from ..utils import (
    oauth_require_read_schema_scope, oauth_require_write_schema_scope
)

if PY3:
    pass


@api.route('/schemas/', methods=['GET', 'POST'])
def api_schemas():
    if request.method == 'GET':
        return _get_schemas()
    if request.method == 'POST':
        return _post_schemas()
    abort(405)


@oauth_require_read_schema_scope
def _get_schemas():
    return respond_success(schemas=[schema.to_json(with_modules=True) for schema in Schema.query])


@oauth_require_write_schema_scope
def _post_schemas():
    with MetaDataSession.begin():
        schema = Schema.create()
        schema.update_from_json(request.json)
        MetaDataSession.add(schema)

    return respond_success(schema=schema.to_json(with_modules=True))


@api.route('/schemas/<schema_uuid>', methods=['GET', 'DELETE'])
def api_schema(schema_uuid):
    if request.method == 'GET':
        return _get_schema(schema_uuid)
    if request.method == 'DELETE':
        return _delete_schema(schema_uuid)
    # SchemaのUpdateはなし
    abort(405)


@oauth_require_read_schema_scope
def _get_schema(schema_uuid):
    schema = Schema.query.get(schema_uuid)
    if not schema:
        return respond_failure('not found', _status=404)

    return respond_success(schema=schema.to_json(with_modules=True))


@oauth_require_write_schema_scope
def _delete_schema(schema_uuid):
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
    # TODO: constants.pyから引っ張ってくる
    property_types = [
        {'name': 'int'},
        {'name': 'float'},
        {'name': 'bool'},
        {'name': 'string'},
        {'name': 'bytes'},
        {'name': 'date'},
        {'name': 'datetime'},
        {'name': 'time'},
        {'name': 'timestamp'},
    ]
    return respond_success(schemaPropertyTypes=property_types)
