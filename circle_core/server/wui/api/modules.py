# -*- coding: utf-8 -*-

"""モジュール関連APIの実装."""

import functools

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

GRAPH_RANGE_TO_TIME_RANGE = {
    '30m': 60 * 30,
    '1h': 60 * 60 * 1,
    '6h': 60 * 60 * 6,
    '1d': 60 * 60 * 24 * 1,
    '7d': 60 * 60 * 24 * 7,
}


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


@api.route('/modules/<uuid:module_uuid>/graph')
def api_module_graph(module_uuid):
    """respond graph data for specified module"""
    module, boxes = _get_module_and_message_boxes(module_uuid)
    if not module:
        return abort(404)

    graph_range = request.args.get('range', '30m')
    if graph_range not in GRAPH_RANGE_TO_TIME_RANGE:
        return abort(400)

    return _respond_rickshaw_graph_data(boxes.values(), graph_range)


@api.route('/modules/<uuid:module_uuid>/<uuid:messagebox_uuid>/graph')
def api_message_box_graph(module_uuid, messagebox_uuid):
    """respond graph data for specified module"""
    module, boxes = _get_module_and_message_boxes(module_uuid)
    if not module or messagebox_uuid not in boxes:
        return abort(404)

    graph_range = request.args.get('range', '30m')
    if graph_range not in GRAPH_RANGE_TO_TIME_RANGE:
        return abort(400)

    return _respond_rickshaw_graph_data([boxes[messagebox_uuid]], graph_range)


def _get_module_and_message_boxes(module_uuid):
    """していされたUUIDのModuleとそのMessageBoxを得る"""
    metadata = get_metadata()
    module = metadata.find_module(module_uuid)
    if module is None:
        return None, None

    boxes = {}
    for box in metadata.message_boxes:
        if box.uuid in module.message_box_uuids:
            boxes[box.uuid] = box

    return module, boxes


def _respond_rickshaw_graph_data(boxes, graph_range):
    import time
    from circle_core.timed_db import TimedDBBundle

    timed_db_bundle = TimedDBBundle(get_metadata().prefix)

    # tz_offset = int(request.args.get('tzOffset', 0))
    tz_offset = 0

    # とりま30m
    time_range = GRAPH_RANGE_TO_TIME_RANGE[graph_range]
    end_time = time.time() - tz_offset
    start_time = end_time - time_range

    graph_data = []
    graph_steps = None
    missing_boxes = []
    for box in boxes:
        db = timed_db_bundle.find_db(box.uuid)
        data = db.fetch(start_time, end_time)
        if not data:
            missing_boxes.append(box)
            continue

        start, end, step, values = data
        if not graph_steps:
            graph_steps = (start, end, step)
        else:
            if graph_steps != (start, end, step):
                raise ValueError('graph range mismatch')

        graph_data.append({
            'messageBox': convert_dict_key_camel_case(box.to_json()),
            'data': [dict(x=x, y=y) for x, y in zip(range(start, end, step), values)],
        })

    if not graph_steps:
        graph_steps = int(start_time), int(end_time), int(end_time - start_time) - 1

    # グラフが無いやつはNullのグラフで埋める
    for box in missing_boxes:
        graph_data.append({
            'messageBox': convert_dict_key_camel_case(box.to_json()),
            'data': [dict(x=x, y=None) for x in range(*graph_steps)],
        })
    graph_data.sort(key=lambda x: x['messageBox']['uuid'])

    return api_jsonify(graphData=graph_data)
