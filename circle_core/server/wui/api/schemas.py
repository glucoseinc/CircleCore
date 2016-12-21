# -*- coding: utf-8 -*-

"""スキーマ関連APIの実装."""

# project module
from .api import api
from ..utils import api_jsonify, get_metadata


@api.route('/schemas/')
def list_schemas():
    metadata = get_metadata()
    schemas = metadata.schemas

    arr = []
    for schema in schemas:
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
        modules = metadata.find_modules_by_schema(schema.uuid)
        dic['modules'] = [{
            'display_name': module.display_name,
            'uuid': str(module.uuid),
        } for module in modules]
        arr.append(dic)
    return api_jsonify(schemas=arr)
