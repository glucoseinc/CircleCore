# -*- coding: utf-8 -*-

"""モジュール関連APIの実装."""

import functools

# community module
from flask import abort, current_app, request
from six import PY3

# project module
# from circle_core.cli.utils import generate_uuid
from circle_core.models import generate_uuid, MessageBox, MetaDataSession, Module, NoResultFound
from .api import api, logger
from .utils import respond_failure
from ..utils import (
    api_jsonify,
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
    response = {
        'modules': [module.to_json(with_boxes=True) for module in Module.query],
    }
    return api_jsonify(**response)


@oauth_require_write_schema_scope
def _post_modules():
    response = {}  # TODO: response形式の統一
    try:
        with MetaDataSession.begin():
            module = Module(uuid=generate_uuid(model=Module))
            module.update_from_json(request.json, with_boxes=True)

            MetaDataSession.add(module)

    except KeyError:
        raise
        return respond_failure('key error', _status=400)

    response['result'] = 'success'
    response['detail'] = {
        'uuid': module.uuid
    }
    return api_jsonify(result='success', detail={'uuid': module.uuid})


@api.route('/modules/<module_uuid>', methods=['GET', 'PUT', 'DELETE'])
def api_module(module_uuid):
    module = Module.query.get(module_uuid)
    if not module:
        return respond_failure('not found', _status=404)

    if request.method == 'GET':
        return _get_module(module)
    if request.method == 'PUT':
        return _put_module(module)
    if request.method == 'DELETE':
        return _delete_module(module)
    abort(405)


@oauth_require_read_schema_scope
def _get_module(module):
    return api_jsonify(module=module.to_json(with_boxes=True, with_schema=True))


@oauth_require_write_schema_scope
def _put_module(module):
    try:
        module.update_from_json(request.json, with_boxes=True)
    except KeyError:
        return respond_failure('key error')

    return api_jsonify(result='success', detail={'uuid': module.uuid})


@oauth_require_write_schema_scope
def _delete_module(module):
    with MetaDataSession.begin():
        MetaDataSession.delete(module)

    return api_jsonify(result='success', detail={'uuid': module.uuid})


@api.route('/modules/<uuid:module_uuid>/graph')
def api_module_graph(module_uuid):
    """respond graph data for specified module"""
    module = Module.query.get(module_uuid)
    if not module:
        raise abort(404)

    graph_range = request.args.get('range', '30m')
    if graph_range not in GRAPH_RANGE_TO_TIME_RANGE:
        return abort(400)

    return _respond_rickshaw_graph_data(module.message_boxes, graph_range)


@api.route('/modules/<uuid:module_uuid>/<uuid:messagebox_uuid>/graph')
def api_message_box_graph(module_uuid, messagebox_uuid):
    """respond graph data for specified module"""
    try:
        box = MessageBox.query.filter_by(uuid=messagebox_uuid, module_uuid=module_uuid).one()
    except NoResultFound:
        raise abort(404)

    graph_range = request.args.get('range', '30m')
    if graph_range not in GRAPH_RANGE_TO_TIME_RANGE:
        return abort(400)

    return _respond_rickshaw_graph_data([box], graph_range)


def _respond_rickshaw_graph_data(boxes, graph_range):
    import time
    from circle_core.timed_db import TimedDBBundle

    timed_db_bundle = TimedDBBundle(current_app.core.prefix)

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
            'messageBox': box.to_json(),
            'data': [dict(x=x, y=y) for x, y in zip(range(start, end, step), values)],
        })

    if not graph_steps:
        graph_steps = int(start_time), int(end_time), int(end_time - start_time) - 1

    # グラフが無いやつはNullのグラフで埋める
    for box in missing_boxes:
        graph_data.append({
            'messageBox': box.to_json(),
            'data': [dict(x=x, y=None) for x in range(*graph_steps)],
        })
    graph_data.sort(key=lambda x: x['messageBox']['uuid'])

    return api_jsonify(graphData=graph_data)
