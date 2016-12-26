# -*- coding: utf-8 -*-

"""スキーマ関連APIの実装."""

# project module
from .api import api
from ..utils import api_jsonify, get_metadata


@api.route('/schemas/')
def list_schemas():
    metadata = get_metadata()
    schemas = metadata.schemas

    arr = [_dictionarify(metadata, schema) for schema in schemas]
    return api_jsonify(schemas=arr)


@api.route('/schemas/<schema_uuid>')
def get_schema(schema_uuid):
    metadata = get_metadata()
    schema = metadata.find_schema(schema_uuid)
    if schema is None:
        return api_jsonify()

    dic = _dictionarify(metadata, schema)
    return api_jsonify(schema=dic)


def _dictionarify(metadata, schema):
    # TODO: metadataにdictを返すようなmethod作成
    dic = {
        'display_name': schema.display_name,
        'uuid': str(schema.uuid),
    }
    properties = schema.properties
    dic['properties'] = [{
        'name': prop.name,
        'type': prop.type,
    } for prop in properties]
    schema_metadata = {
        'memo': 'mock memo'  # TODO: memo
    }
    dic['metadata'] = schema_metadata
    modules = metadata.find_modules_by_schema(schema.uuid)
    dic['modules'] = [{
        'display_name': module.display_name,
        'uuid': str(module.uuid),
    } for module in modules]
    return dic
