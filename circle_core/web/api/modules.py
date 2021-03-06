# -*- coding: utf-8 -*-
"""モジュール関連APIの実装."""
from typing import TYPE_CHECKING
from uuid import UUID

# community module
from flask import abort, current_app, request

# project module
from circle_core.models import MessageBox, MetaDataSession, Module, NoResultFound

from .api import api
from .utils import respond_failure, respond_success
from ..utils import (oauth_require_read_schema_scope, oauth_require_write_schema_scope)

if TYPE_CHECKING:
    from flask import Response

GRAPH_RANGE_TO_TIME_RANGE = {
    '30m': 60 * 30,
    '1h': 60 * 60 * 1,
    '6h': 60 * 60 * 6,
    '1d': 60 * 60 * 24 * 1,
    '7d': 60 * 60 * 24 * 7,
}


@api.route('/modules/', methods=['GET', 'POST'])
def api_modules():
    """全てのModuleのCRUD."""
    if request.method == 'GET':
        return _get_modules()
    if request.method == 'POST':
        return _post_modules()
    abort(405)


@oauth_require_read_schema_scope
def _get_modules() -> 'Response':
    """全てのModuleの情報を取得する.

    :return: 全てのModuleの情報
    :rtype: Response
    """
    return respond_success(modules=[module.to_json(with_boxes=True, with_cc_info=True) for module in Module.query])


@oauth_require_write_schema_scope
def _post_modules() -> 'Response':
    """Moduleを作成する.

    :return: 作成したModuleの情報
    :rtype: Response
    """
    try:
        with MetaDataSession.begin():
            module = Module.create()
            module.update_from_json(request.json, with_boxes=True)

            MetaDataSession.add(module)

    except KeyError:
        raise
        return respond_failure('key error', _status=400)

    return respond_success(module=module.to_json(with_boxes=True, with_schema=True))


@api.route('/modules/<module_uuid>', methods=['GET', 'PUT', 'DELETE'])
def api_module(module_uuid):
    """単一のModuleのCRUD."""
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
    """Moduleの情報を取得する.

    :param Module module: 取得するModule
    :return: Moduleの情報
    :rtype: Response
    """
    return respond_success(module=module.to_json(with_boxes=True, with_schema=True, with_cc_info=True))


@oauth_require_write_schema_scope
def _put_module(module):
    """Moduleを更新する.

    :param Module module: 更新するModule
    :return: Moduleの情報
    :rtype: Response
    """
    try:
        with MetaDataSession.begin():
            module.update_from_json(request.json, with_boxes=True)
            MetaDataSession.add(module)
    except KeyError:
        return respond_failure('key error')
    except ValueError as e:
        return respond_failure(str(e))

    return respond_success(module=module.to_json(with_boxes=True, with_schema=True))


@oauth_require_write_schema_scope
def _delete_module(module):
    """Moduleを削除する.

    :param Module module: 削除するModule
    :return: Moduleの情報
    :rtype: Response
    """
    with MetaDataSession.begin():
        if module.replication_master is not None:
            MetaDataSession.delete(module.replication_master)
        else:
            MetaDataSession.delete(module)

    return respond_success(module={'uuid': module.uuid})


@api.route('/modules/<uuid:module_uuid>/graph')
def api_module_graph(module_uuid):
    """respond graph data for specified module."""
    module = Module.query.get(module_uuid)
    if not module:
        raise abort(404)

    graph_range = request.args.get('range', '30m')
    if graph_range not in GRAPH_RANGE_TO_TIME_RANGE:
        return abort(400)

    return _respond_rickshaw_graph_data(module.message_boxes, graph_range)


@api.route('/modules/<uuid:module_uuid>/<uuid:messagebox_uuid>/graph')
def api_message_box_graph(module_uuid, messagebox_uuid):
    """respond graph data for specified module."""
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
    graph_data = fetch_rickshaw_graph_data(boxes, graph_range, timed_db_bundle, time.time() - tz_offset)
    return respond_success(graphData=graph_data)


def fetch_rickshaw_graph_data(boxes, graph_range, timed_db_bundle, end_time):
    assert graph_range in GRAPH_RANGE_TO_TIME_RANGE
    # とりま30m
    time_range = GRAPH_RANGE_TO_TIME_RANGE[graph_range]
    start_time = end_time - time_range

    graph_data = []
    graph_steps = None
    missing_boxes = []
    for box in boxes:
        box_uuid = box if isinstance(box, UUID) else box.uuid
        db = timed_db_bundle.find_db(box_uuid)
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

        for idx, value in enumerate(values):
            values[idx] = value or 0

        graph_data.append(
            {
                'messageBox': dict(uuid=str(box_uuid)) if isinstance(box, UUID) else box.to_json(),
                'data': [dict(x=x, y=y) for x, y in zip(range(start, end, step), values)],
            }
        )

    if not graph_steps:
        graph_steps = int(start_time), int(end_time), int(end_time - start_time) - 1

    # グラフが無いやつはNullのグラフで埋める
    for box in missing_boxes:
        graph_data.append(
            {
                'messageBox': dict(uuid=str(box_uuid)) if isinstance(box, UUID) else box.to_json(),
                'data': [dict(x=x, y=None) for x in range(*graph_steps)],
            }
        )
    graph_data.sort(key=lambda x: x['messageBox']['uuid'])

    return graph_data


@api.route('/modules/<uuid:module_uuid>/<uuid:messagebox_uuid>/data')
def api_message_box_data(module_uuid, messagebox_uuid):
    """respond data for specified module."""
    try:
        box = MessageBox.query.filter_by(uuid=messagebox_uuid, module_uuid=module_uuid).one()
    except NoResultFound:
        raise abort(404)

    output_format = request.args.get('format', 'json')
    if output_format not in ('json',):
        raise abort(400)

    query = {}
    limit = request.args.get('limit', None)
    if limit:
        limit = int(limit, 10)
        query['limit'] = limit

    database = current_app.core.get_database()
    messages = []
    for m in database.enum_messages(box, limit=limit, order='desc'):
        messages.append(m.to_json(with_boxid=False))

    return respond_success(
        messages=messages,
        query=query,
        schema=box.schema.to_json(),
        # total=database.count_messages(box),
    )
