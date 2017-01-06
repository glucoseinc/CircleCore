# -*- coding: utf-8 -*-

"""モジュール関連APIの実装."""

# community module
from flask import abort, request
from six import PY3

# project module
from circle_core.cli.utils import generate_uuid
from circle_core.models import MessageBox, Module
from .api import api
from ..utils import api_jsonify, convert_dict_key_camel_case, convert_dict_key_snake_case, get_metadata

if PY3:
    from typing import Any, Dict


@api.route('/modules/', methods=['GET', 'POST'])
def api_modules():
    if request.method == 'GET':
        return _get_modules()
    if request.method == 'POST':
        return _post_modules()
    abort(405)


def _get_modules():
    metadata = get_metadata()
    modules = metadata.modules

    response = {
        'modules': [_dictify(module) for module in modules],
    }
    return api_jsonify(**convert_dict_key_camel_case(response))


def _post_modules():
    metadata = get_metadata()
    dic = convert_dict_key_snake_case(request.json)
    response = {}  # TODO: response形式の統一

    try:
        message_boxes = []
        message_box_dics = dic['message_boxes']
        for message_box_dic in message_box_dics:
            display_name = message_box_dic['display_name']
            if len(display_name) == 0:
                display_name = None
            schema_dic = message_box_dic['schema']
            schema_uuid = schema_dic['uuid']
            description = message_box_dic['description']
            message_box_uuid = generate_uuid(existing=[_message_box.uuid for _message_box in metadata.message_boxes])
            message_box = MessageBox(message_box_uuid, schema_uuid, display_name, description)
            message_boxes.append(message_box)

        display_name = dic['display_name']
        if len(display_name) == 0:
            display_name = None
        tags = ','.join(dic['tags'])
        description = dic['description']
        if len(description) == 0:
            description = None
    except KeyError:
        response['result'] = 'failure'
        response['detail'] = {
            'reason': 'key error'
        }
        return api_jsonify(**response)

    message_box_uuids = ','.join([str(_message_box.uuid) for _message_box in message_boxes])
    module_uuid = generate_uuid(existing=[module.uuid for module in metadata.modules])
    module = Module(
        module_uuid,
        message_box_uuids,  # TODO: 引き渡すmessage_box_uuidsはリスト化
        display_name,
        tags,
        description)

    for message_box in message_boxes:
        metadata.register_message_box(message_box)
    metadata.register_module(module)
    response['result'] = 'success'
    response['detail'] = {
        'uuid': module_uuid
    }
    return api_jsonify(**convert_dict_key_camel_case(response))


@api.route('/modules/<module_uuid>', methods=['GET', 'DELETE'])
def api_module(module_uuid):
    if request.method == 'GET':
        return _get_module(module_uuid)
    if request.method == 'PUT':
        return _put_module(module_uuid)
    if request.method == 'DELETE':
        return _delete_module(module_uuid)
    abort(405)


def _get_module(module_uuid):
    metadata = get_metadata()
    module = metadata.find_module(module_uuid)
    if module is None:
        return api_jsonify()  # TODO: return failure

    response = {
        'module': _dictify(module)
    }
    return api_jsonify(**convert_dict_key_camel_case(response))


def _put_module(module_uuid):
    # TODO: Implement
    response = {}  # TODO: response形式の統一
    response['result'] = 'failure'
    response['detail'] = {
        'reason': 'not implemented'
    }
    return api_jsonify(**convert_dict_key_camel_case(response))


def _delete_module(module_uuid):
    metadata = get_metadata()
    response = {}  # TODO: response形式の統一
    module = metadata.find_module(module_uuid)
    if module is None:
        response['result'] = 'failure'
        response['detail'] = {
            'reason': 'not found'
        }
        return api_jsonify(**convert_dict_key_camel_case(response))

    metadata.unregister_module(module)
    # TODO: messageBoxも消す -> unregister_moduleで一緒にやる
    response['result'] = 'success'
    response['detail'] = {
        'uuid': module_uuid
    }
    return api_jsonify(**convert_dict_key_camel_case(response))


def _dictify(module):
    """TODO: metadataにdictを返すようなmethod作成.

    :param Module module: Module
    :return: 辞書
    :rtype: Dict[str, Any]
    """
    metadata = get_metadata()
    dic = {
        'uuid': str(module.uuid),
        'display_name': module.display_name,
        'tags': module.tags,
        'description': module.description,
    }
    message_boxes = [message_box for message_box in metadata.message_boxes
                     if message_box.uuid in module.message_box_uuids]
    dictified_message_boxes = []
    for message_box in message_boxes:
        schema = metadata.find_schema(message_box.schema_uuid)
        dictified_schema = {
            'uuid': str(schema.uuid),
            'display_name': schema.display_name,
            'properties': schema.dictified_properties,
            'memo': schema.memo,
        } if schema is not None else None
        dictified_message_box = {
            'uuid': str(message_box.uuid),
            'display_name': message_box.display_name,
            'description': message_box.description,
            'schema': dictified_schema,
        }
        dictified_message_boxes.append(dictified_message_box)
    dic['message_boxes'] = dictified_message_boxes
    return dic
