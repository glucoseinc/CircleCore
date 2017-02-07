# -*- coding: utf-8 -*-

"""スキーマ関連APIの実装."""

# community module
from flask import abort, request
from six import PY3

# project module
# from circle_core.cli.utils import generate_uuid
from circle_core.models import Schema
from .api import api
from ..utils import (
    api_jsonify, api_response_failure,
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
    response = {
        'schemas': [schema.to_json(with_modules=True) for schema in Schema.query],
    }
    return api_jsonify(**response)


@oauth_require_write_schema_scope
def _post_schemas():
    dic = convert_dict_key_snake_case(request.json)
    response = {}  # TODO: response形式の統一
    try:
        display_name = dic['display_name']
        properties = dic['properties']
        properties = [prop for prop in properties
                      if len(prop['name']) != 0 and len(prop['type']) != 0]
        memo = dic['memo']
        if len(memo) == 0:
            memo = None
    except KeyError:
        return api_response_failure('key error')

    metadata = get_metadata()
    schema_uuid = generate_uuid(existing=[schema.uuid for schema in metadata.schemas])
    schema = Schema(schema_uuid, display_name, properties, memo)
    metadata.register_schema(schema)
    response['result'] = 'success'
    response['detail'] = {
        'uuid': schema_uuid
    }
    return api_jsonify(**convert_dict_key_camel_case(response))


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
    metadata = get_metadata()

    response = {
        'schema': metadata.json_schema_with_module(schema_uuid)
    }
    return api_jsonify(**convert_dict_key_camel_case(response))


@oauth_require_write_schema_scope
def _delete_schema(schema_uuid):
    metadata = get_metadata()
    response = {}  # TODO: response形式の統一
    schema = metadata.find_schema(schema_uuid)
    if schema is None:
        return api_response_failure('not found')

    attached_modules = metadata.find_modules_by_schema(schema_uuid)
    if len(attached_modules) != 0:
        reason = 'module {uuids} {verb} attached'.format(
            uuids=', '.join([str(module.uuid) for module in attached_modules]),
            verb='is' if len(attached_modules) == 1 else 'are'
        )
        return api_response_failure(reason)

    metadata.unregister_schema(schema)
    response['result'] = 'success'
    response['detail'] = {
        'uuid': schema_uuid
    }
    return api_jsonify(**convert_dict_key_camel_case(response))


@api.route('/schemas/propertytypes')
@oauth_require_read_schema_scope
def api_get_property_types():
    # TODO: constants.pyから引っ張ってくる
    response = {
        'schema_property_types': [
            {'name': 'int'},
            {'name': 'float'},
            {'name': 'bool'},
            {'name': 'string'},
            {'name': 'bytes'},
            {'name': 'date'},
            {'name': 'datetime'},
            {'name': 'time'},
            {'name': 'timestamp'},
        ],
    }
    return api_jsonify(**convert_dict_key_camel_case(response))
