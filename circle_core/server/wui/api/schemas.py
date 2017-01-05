# -*- coding: utf-8 -*-

"""スキーマ関連APIの実装."""

# community module
from flask import abort, request
from six import PY3

# project module
from circle_core.cli.utils import generate_uuid
from circle_core.models import Schema
from .api import api
from ..utils import api_jsonify, camel_case, get_metadata, snake_case

if PY3:
    from typing import Any, Dict


@api.route('/schemas/', methods=['GET', 'POST'])
def api_schemas():
    if request.method == 'GET':
        return _get_schemas()
    if request.method == 'POST':
        return _post_schemas()
    abort(405)


def _get_schemas():
    metadata = get_metadata()
    schemas = metadata.schemas

    response = {
        'schemas': [_dictify(schema) for schema in schemas],
    }
    return api_jsonify(**camel_case(response))


def _post_schemas():
    dic = snake_case(request.json)
    response = {}  # TODO: response形式の統一
    try:
        display_name = dic['display_name']
        if len(display_name) == 0:
            display_name = None
        properties = dic['properties']
        properties = [prop for prop in properties
                      if len(prop['name']) != 0 and len(prop['type']) != 0]
        memo = dic['metadata']['memo']
        if len(memo) == 0:
            memo = None
    except KeyError:
        response['result'] = 'failure'
        response['detail'] = {
            'reason': 'key error'
        }
        return api_jsonify(**camel_case(response))

    metadata = get_metadata()
    schema_uuid = generate_uuid(existing=[schema.uuid for schema in metadata.schemas])
    schema = Schema(schema_uuid, display_name, properties, memo)
    metadata.register_schema(schema)
    response['result'] = 'success'
    response['detail'] = {
        'uuid': schema_uuid
    }
    return api_jsonify(**camel_case(response))


@api.route('/schemas/<schema_uuid>', methods=['GET', 'DELETE'])
def api_schema(schema_uuid):
    if request.method == 'GET':
        return _get_schema(schema_uuid)
    if request.method == 'DELETE':
        return _delete_schema(schema_uuid)
    # SchemaのUpdateはなし
    abort(405)


def _get_schema(schema_uuid):
    metadata = get_metadata()
    schema = metadata.find_schema(schema_uuid)
    if schema is None:
        return api_jsonify()  # TODO: return failure

    response = {
        'schema': _dictify(schema)
    }
    return api_jsonify(**camel_case(response))


def _delete_schema(schema_uuid):
    metadata = get_metadata()
    response = {}  # TODO: response形式の統一
    schema = metadata.find_schema(schema_uuid)
    if schema is None:
        response['result'] = 'failure'
        response['detail'] = {
            'reason': 'not found'
        }
        return api_jsonify(**camel_case(response))

    attached_modules = metadata.find_modules_by_schema(schema_uuid)
    if len(attached_modules) != 0:
        response['result'] = 'failure'
        response['detail'] = {
            'reason': 'module {uuids} {verb} attached'.format(
                uuids=', '.join([str(module.uuid) for module in attached_modules]),
                verb='is' if len(attached_modules) == 1 else 'are'
            )
        }
        return api_jsonify(**camel_case(response))

    metadata.unregister_schema(schema)
    response['result'] = 'success'
    response['detail'] = {
        'uuid': schema_uuid
    }
    return api_jsonify(**camel_case(response))


def _dictify(schema):
    """TODO: metadataにdictを返すようなmethod作成.

    :param Schema schema: Schema
    :return: 辞書
    :rtype: Dict[str, Any]
    """
    metadata = get_metadata()
    dic = {
        'display_name': schema.display_name,
        'uuid': str(schema.uuid),
        'properties': schema.dictified_properties,
        'metadata': {
            'memo': schema.memo
        }
    }
    modules = metadata.find_modules_by_schema(schema.uuid)
    dic['modules'] = [{
        'display_name': module.display_name,
        'uuid': str(module.uuid),
    } for module in modules]
    return dic


@api.route('/schemas/propertytypes')
def api_get_property_types():
    # TODO: constants.pyから引っ張ってくる
    response = {
        'property_types': [
            {'name': 'int'},
            {'name': 'float'},
            {'name': 'text'},
        ],
    }
    return api_jsonify(**camel_case(response))
