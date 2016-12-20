# -*- coding: utf-8 -*-
import json
from multiprocessing import Process
from os import environ
from uuid import UUID

from click.testing import CliRunner
import pytest
from sqlalchemy import create_engine
from sqlalchemy.engine.reflection import Inspector
from sqlalchemy.types import INTEGER, TIMESTAMP
from tornado.ioloop import IOLoop
from tornado.testing import AsyncHTTPTestCase, gen_test
from tornado.web import Application
from tornado.websocket import websocket_connect, WebSocketHandler

from circle_core.cli.cli_main import cli_main
from circle_core.database import Database
from circle_core.models.module import Module
from circle_core.models.schema import Schema
from circle_core.server.ws import ReplicationHandler, SensorHandler


class DummyReplicationMaster(WebSocketHandler):
    def on_message(self, message):
        if json.loads(message) == {'command': 'MIGRATE'}:
            res = json.dumps({
                'modules': [{
                    'uuid': '8e654793-5c46-4721-911e-b9d19f0779f9',
                    'schema_uuid': '44ae2fd8-52d0-484d-9a48-128b07937a0a',
                    'display_name': 'DummyModule',
                    'properties': 'foo:bar'
                }],
                'schemas': [{
                    'uuid': '44ae2fd8-52d0-484d-9a48-128b07937a0a',
                    'display_name': 'DummySchema',
                    'properties': 'hoge:int'
                }]
            })
            self.write_message(res)


def start_dummy_server():
    Application([(r'/replication/(?P<slave_uuid>[0-9A-Fa-f-]+)', DummyReplicationMaster)]).listen(5001)
    IOLoop.current().start()


def setup_module(module):
    global server
    server = Process(target=start_dummy_server)
    server.start()


def teardown_module(module):
    global server
    server.terminate()


@pytest.mark.usefixtures('mysql')
def test_migrate(mysql):
    result = CliRunner().invoke(cli_main, ['replication', 'add', 'localhost:5001', '--database', mysql.url])
    assert result.exit_code == 0

    db = Database(mysql.url)
    engine = create_engine(mysql.url)
    inspector = Inspector.from_engine(engine)
    module = Module(
        '8e654793-5c46-4721-911e-b9d19f0779f9',
        '44ae2fd8-52d0-484d-9a48-128b07937a0a',
        'DummyModule',
        'foo:bar'
    )
    table_name = db.make_table_name_for_module(module)
    columns = inspector.get_columns(table_name)
    types = {
        '_created_at': TIMESTAMP,
        '_counter': INTEGER,
        'hoge': INTEGER
    }

    for column in columns:
        assert isinstance(column['type'], types[column['name']])
