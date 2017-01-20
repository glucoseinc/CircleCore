# -*- coding: utf-8 -*-

"""モジュール関連APIの実装."""

# community module
from flask import abort, request
from six import PY3

# project module
from circle_core.cli.utils import generate_uuid
from circle_core.models import MessageBox, Module
from .api import api
from ..utils import (
    api_jsonify, api_response_failure, convert_dict_key_camel_case, convert_dict_key_snake_case, get_metadata,
    oauth_require_read_schema_scope, oauth_require_write_schema_scope
)

if PY3:
    from typing import Dict, List


@api.route('/modules/', methods=['GET', 'POST'])
def api_modules():
    if request.method == 'GET':
        return _get_modules()
    if request.method == 'POST':
        return _post_modules()
    abort(405)


@oauth_require_read_schema_scope
def _get_modules():
    metadata = get_metadata()

    response = {
        'modules': [metadata.denormalize_json_module(module.uuid) for module in metadata.modules],
    }
    return api_jsonify(**convert_dict_key_camel_case(response))


@oauth_require_write_schema_scope
def _post_modules():
    response = {}  # TODO: response形式の統一
    try:
        message_boxes = _create_message_boxes_from_request_json(request.json)
        message_box_uuids = [message_box.uuid for message_box in message_boxes]
        module = _create_module_from_request_json(request.json, message_box_uuids)
    except KeyError:
        return api_response_failure('key error')

    metadata = get_metadata()
    for message_box in message_boxes:
        metadata.register_message_box(message_box)
    metadata.register_module(module)
    response['result'] = 'success'
    response['detail'] = {
        'uuid': module.uuid
    }
    return api_jsonify(**convert_dict_key_camel_case(response))


@api.route('/modules/<module_uuid>', methods=['GET', 'PUT', 'DELETE'])
def api_module(module_uuid):
    if request.method == 'GET':
        return _get_module(module_uuid)
    if request.method == 'PUT':
        return _put_module(module_uuid)
    if request.method == 'DELETE':
        return _delete_module(module_uuid)
    abort(405)


@oauth_require_read_schema_scope
def _get_module(module_uuid):
    metadata = get_metadata()

    response = {
        'module': metadata.denormalize_json_module(module_uuid)
    }
    return api_jsonify(**convert_dict_key_camel_case(response))


@oauth_require_write_schema_scope
def _put_module(module_uuid):
    response = {}  # TODO: response形式の統一
    try:
        message_boxes = _create_message_boxes_from_request_json(request.json)
        message_box_uuids = [message_box.uuid for message_box in message_boxes]
        module = _create_module_from_request_json(request.json, message_box_uuids)
    except KeyError:
        return api_response_failure('key error')

    metadata = get_metadata()

    old_module = metadata.find_module(module.uuid)
    if old_module is None:
        return api_response_failure('module uuid invalid')

    old_message_box_uuids = old_module.message_box_uuids

    deleting_message_box_uuids = list(set(old_message_box_uuids).difference(set(message_box_uuids)))
    creating_message_box_uuids = list(set(message_box_uuids).difference(set(old_message_box_uuids)))
    updating_message_box_uuids = list(set(message_box_uuids).intersection(set(old_message_box_uuids)))

    all_message_box_uuids = [message_box.uuid for message_box in metadata.message_boxes]

    if len(set(updating_message_box_uuids).difference(all_message_box_uuids)) != 0:
        return api_response_failure('message box uuid invalid')

    for creating_message_box_uuid in creating_message_box_uuids:
        creating_message_box = [message_box for message_box in message_boxes
                                if message_box.uuid == creating_message_box_uuid][0]
        metadata.register_message_box(creating_message_box)
    for deleting_message_box_uuid in deleting_message_box_uuids:
        deleting_message_box = metadata.find_message_box(deleting_message_box_uuid)
        metadata.unregister_message_box(deleting_message_box)
    for updating_message_box_uuid in updating_message_box_uuids:
        updating_message_box = [message_box for message_box in message_boxes
                                if message_box.uuid == updating_message_box_uuid][0]
        old_updating_message_box = metadata.find_message_box(updating_message_box_uuid)
        if updating_message_box != old_updating_message_box:
            metadata.update_message_box(updating_message_box)
    if module != old_module:
        metadata.update_module(module)

    response['result'] = 'success'
    response['detail'] = {
        'uuid': module.uuid
    }
    return api_jsonify(**convert_dict_key_camel_case(response))


@oauth_require_write_schema_scope
def _delete_module(module_uuid):
    metadata = get_metadata()
    response = {}  # TODO: response形式の統一
    module = metadata.find_module(module_uuid)
    if module is None:
        response['detail'] = {
            'reason': 'not found'
        }
        return api_response_failure('not found')

    metadata.unregister_module(module)
    # TODO: messageBoxも消す -> unregister_moduleで一緒にやる
    response['result'] = 'success'
    response['detail'] = {
        'uuid': module_uuid
    }
    return api_jsonify(**convert_dict_key_camel_case(response))


def _create_module_from_request_json(request_json, message_box_uuids):
    """Create module from json.

    :param Dict request_json:
    :param List[UUID] message_box_uuids:
    :return: Module
    :rtype: Module
    """
    metadata = get_metadata()
    dic = convert_dict_key_snake_case(request_json)

    display_name = dic['display_name']
    if len(display_name) == 0:
        display_name = None
    tags = ','.join(dic['tags'])
    memo = dic['memo']
    if len(memo) == 0:
        memo = None

    module_uuid = dic['uuid']
    if module_uuid == '':
        module_uuid = generate_uuid(existing=[module.uuid for module in metadata.modules])
    module = Module(
        module_uuid,
        message_box_uuids,
        display_name,
        tags,
        memo)

    return module


def _create_message_boxes_from_request_json(request_json):
    """Create message boxes from json.

    :param Dict request_json:
    :return: MessageBoxes
    :rtype: List[MessageBox]
    """
    metadata = get_metadata()
    dic = convert_dict_key_snake_case(request_json)

    message_boxes = []
    message_box_dics = dic['message_boxes']
    for message_box_dic in message_box_dics:
        display_name = message_box_dic['display_name']
        if len(display_name) == 0:
            display_name = None
        schema_uuid = message_box_dic['schema']
        memo = message_box_dic['memo']
        message_box_uuid = message_box_dic['uuid']
        if message_box_uuid == '':
            message_box_uuid = generate_uuid(existing=[_message_box.uuid for _message_box in metadata.message_boxes])
        message_box = MessageBox(message_box_uuid, schema_uuid, display_name, memo)
        message_boxes.append(message_box)

    return message_boxes
