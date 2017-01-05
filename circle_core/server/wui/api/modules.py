# -*- coding: utf-8 -*-

"""モジュール関連APIの実装."""

# community module
from flask import abort, request
from six import PY3

# project module
from circle_core.cli.utils import generate_uuid
from circle_core.models import Module
from .api import api
from ..utils import api_jsonify, camel_case, snake_case, get_metadata

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
    return api_jsonify(**camel_case(response))


def _post_modules():
    dic = snake_case(request.json)
    response = {}  # TODO: response形式の統一
    # TODO: message_boxの処理
    message_box_uuids = ''
    try:
        display_name = dic['display_name']
        if len(display_name) == 0:
            display_name = None
        tags = dic['metadata']['tags']
        description = dic['metadata']['description']
        if len(description) == 0:
            description = None
    except KeyError:
        response['result'] = 'failure'
        response['detail'] = {
            'reason': 'key error'
        }
        return api_jsonify(**response)

    metadata = get_metadata()
    module_uuid = generate_uuid(existing=[module.uuid for module in metadata.modules])
    module = Module(
        module_uuid,
        message_box_uuids,  # TODO: 引き渡すmessage_box_uuidsはリスト化
        display_name,
        tags,
        description)
    metadata.register_module(module)
    response['result'] = 'success'
    response['detail'] = {
        'uuid': module_uuid
    }
    return api_jsonify(**camel_case(response))


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
    return api_jsonify(**camel_case(response))


def _put_module(module_uuid):
    # TODO: Implement
    response = {}  # TODO: response形式の統一
    response['result'] = 'failure'
    response['detail'] = {
        'reason': 'not implemented'
    }
    return api_jsonify(**camel_case(response))


def _delete_module(module_uuid):
    metadata = get_metadata()
    response = {}  # TODO: response形式の統一
    module = metadata.find_module(module_uuid)
    if module is None:
        response['result'] = 'failure'
        response['detail'] = {
            'reason': 'not found'
        }
        return api_jsonify(**camel_case(response))

    metadata.unregister_module(module)
    # TODO: messageBoxも消す -> unregister_moduleで一緒にやる
    response['result'] = 'success'
    response['detail'] = {
        'uuid': module_uuid
    }
    return api_jsonify(**camel_case(response))


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
        'metadata': {
            'tags': module.tags,
            'description': module.description
        }
    }
    message_boxes = [message_box for message_box in metadata.message_boxes
                     if message_box.uuid in module.message_box_uuids]
    dic['message_boxes'] = [{
        'uuid': str(message_box.uuid),
        'display_name': message_box.display_name,
        'description': message_box.description,
        'schema': {
            'uuid': str(message_box.schema_uuid)  # TODO: Schemaの他情報も構築する？
        }
    } for message_box in message_boxes]
    return dic
