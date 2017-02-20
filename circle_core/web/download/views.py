# -*- coding: utf-8 -*-
"""ダウンロード."""

# system module
import time

# community module
from dateutil import parser
from flask import abort, current_app, request, Response

# project module
from circle_core.models import MessageBox, NoResultFound
from .download import download


@download.route('/modules/<uuid:module_uuid>/<uuid:message_box_uuid>/data')
def download_message_box_data(module_uuid, message_box_uuid):
    try:
        box = MessageBox.query.filter_by(uuid=message_box_uuid, module_uuid=module_uuid).one()
    except NoResultFound:
        raise abort(404)

    start = request.args.get('start', None)
    if start:
        start = time.mktime(parser.parse(start).timetuple())

    end = request.args.get('end', None)
    if end:
        end = time.mktime(parser.parse(end).timetuple())

    database = current_app.core.get_database()

    message_generator = database.enum_messages(box, start=start, end=end)

    def generate():
        def to_line(row):
            return ','.join([str(c) for c in row]) + '\n'

        def to_data_line(m):
            return to_line(
                [m.timestamp, m.counter] + [m.payload.get(key, '') for key in payload_keys]
            )

        message = next(message_generator)
        payload_keys = sorted(list(message.payload.keys()))
        header = ['timestamp', 'counter'] + payload_keys
        yield to_line(header)

        yield to_data_line(message)
        for message in message_generator:
            yield to_data_line(message)

    filename = '{}_{}.csv'.format(module_uuid, message_box_uuid)
    headers = {
        'Content-Disposition': 'attachment; filename={}'.format(filename),
    }
    return Response(generate(), mimetype='text/csv', headers=headers)
