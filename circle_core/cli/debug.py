# -*- coding: utf-8 -*-

"""CLI debug commands."""

# system module
import datetime
import math
from uuid import UUID
import time

# community module
from base58 import b58decode
from dateutil import parser
import click
from six import PY3

from circle_core.timed_db import TimedDBBundle


if PY3:
    from typing import List, Tuple


@click.group('debug')
def cli_debug():
    """`crcr debug`の起点."""
    pass


@cli_debug.command('build_whisper')
@click.argument('dir')
@click.argument('dburl')
@click.argument('table')
@click.argument('end_date')
def build_whisper(dir, dburl, table, end_date):
    import sqlalchemy as sa

    engine = sa.create_engine(dburl)
    connection = engine.connect()

    time_db_bundle = TimedDBBundle(dir)
    box_id = UUID(int=0)

    try:
        end = int(end_date)
    except ValueError:
        end = time.mktime(parser.parse(end_date).timetuple())

    query = '''\
SELECT _created_at, _counter FROM `{table}` WHERE _created_at < {end} ORDER BY _created_at ASC, _counter ASC
'''.format(table=table, end=end)

    updates = []
    for _created_at, _counter in connection.execute(query):
        t = math.floor(_created_at)

        if len(updates) > 4096 and math.floor(updates[-1][1]) != t:
            # commit
            print(math.floor(updates[-1][1]), len(updates))
            time_db_bundle.update(updates)
            updates = []

        updates.append((box_id, _created_at))

    if updates:
        time_db_bundle.update(updates)


@cli_debug.command()
@click.argument('dir')
@click.argument('box_id')
@click.argument('end_time', type=float)
@click.argument('graph_range')
def dump_whisper(dir, box_id, end_time, graph_range):
    from circle_core.web.api.modules import fetch_rickshaw_graph_data

    time_db_bundle = TimedDBBundle(dir)
    graph_data = fetch_rickshaw_graph_data([UUID(box_id)], graph_range, time_db_bundle, end_time)
    print(graph_data)

    time_db = time_db_bundle.find_db(UUID(box_id))
    # time_db
