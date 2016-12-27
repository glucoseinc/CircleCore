# -*- coding: utf-8 -*-
import json
from multiprocessing import Process
from os import environ
from time import sleep
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
from circle_core.models.message_box import MessageBox
from circle_core.models.metadata.base import MetadataReader
from circle_core.models.module import Module
from circle_core.models.schema import Schema
from circle_core.server.ws import ReplicationHandler, SensorHandler
from circle_core.workers import replicator
from circle_core.workers.replicator import Replicator


class DummyMetadata(MetadataReader):
    schemas = [Schema('95eef02e-36e5-446e-9fea-aedd10321f6f', 'json', 'hoge:int')]
    message_boxes = [MessageBox('402a7a37-691d-40ed-b0fe-4aeed9d0bba1', '95eef02e-36e5-446e-9fea-aedd10321f6f')]
    modules = [Module(
        '314a578a-6543-4331-90f7-ed80c81d29bf',
        '402a7a37-691d-40ed-b0fe-4aeed9d0bba1',
        'DummyModule',
        'foo,bar'
    )]
    users = []
    parse_url_scheme = None
    writable = True

    def register_schema(self, schema):  # TODO: こういうのをMockにするべきなのかな
        self.schemas.append(schema)

    def register_message_box(self, box):
        self.message_boxes.append(box)

    def register_module(self, module):
        self.modules.append(module)


def setup_module(module):
    replicator.get_uuid = lambda: '5c8fe778-1cb8-4a92-8f5d-588990a19def'
    replicator.metadata = DummyMetadata


def teardown_module(module):
    global worker
    worker.terminate()


def start_worker(mysql):
    global worker
    sleep(0.5)

    class DummyMetadata(object):
        database_url = mysql.url

    worker = Process(target=lambda: Replicator(DummyMetadata, 'localhost:5001').run())
    worker.start()


class DummyReplicationMaster(WebSocketHandler):
    def on_message(self, message):
        msg = json.loads(message)
        if msg == {'command': 'MIGRATE'}:
            res = json.dumps({
                'modules': [{
                    'uuid': '8e654793-5c46-4721-911e-b9d19f0779f9',
                    'message_box_uuids': '316720eb-84fe-43b3-88b7-9aad49a93220',
                    'display_name': 'DummyModule',
                    'tags': 'foo,bar'
                }],
                'message_boxes': [{
                    'uuid': '316720eb-84fe-43b3-88b7-9aad49a93220',
                    'schema_uuid': '44ae2fd8-52d0-484d-9a48-128b07937a0a'
                }],
                'schemas': [{
                    'uuid': '44ae2fd8-52d0-484d-9a48-128b07937a0a',
                    'display_name': 'DummySchema',
                    'properties': 'hoge:int'
                }]
            })
            self.write_message(res)
        elif msg == {'command': 'RECEIVE'}:
            IOLoop.current().stop()


@pytest.mark.timeout(1)
@pytest.mark.usefixtures('mysql')
def test_migrate(mysql):
    start_worker(mysql)
    Application([
        (r'/replication/(?P<slave_uuid>[0-9A-Fa-f-]+)', DummyReplicationMaster)
    ], mysql=mysql, debug=True).listen(5001)
    IOLoop.current().start()

    assert filter(lambda schema: schema.uuid == UUID('8e654793-5c46-4721-911e-b9d19f0779f9'), DummyMetadata.schemas)
    assert filter(lambda box: box.uuid == UUID('316720eb-84fe-43b3-88b7-9aad49a93220'), DummyMetadata.message_boxes)
    assert filter(lambda module: module.uuid == UUID('8e654793-5c46-4721-911e-b9d19f0779f9'), DummyMetadata.modules)

    db = Database(mysql.url)
    engine = create_engine(mysql.url)
    inspector = Inspector.from_engine(engine)
    box = MessageBox('316720eb-84fe-43b3-88b7-9aad49a93220', '44ae2fd8-52d0-484d-9a48-128b07937a0a')
    table_name = db.make_table_name_for_message_box(box)
    columns = inspector.get_columns(table_name)
    types = {
        '_created_at': TIMESTAMP,
        '_counter': INTEGER,
        'hoge': INTEGER
    }

    for column in columns:
        assert isinstance(column['type'], types[column['name']])
