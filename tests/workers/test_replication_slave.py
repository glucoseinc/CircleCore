# -*- coding: utf-8 -*-
from datetime import datetime
import json
from multiprocessing import Process
from os import environ
from threading import Thread
from time import sleep, time
from uuid import UUID

from click.testing import CliRunner
import pytest
from sqlalchemy import create_engine, Table
from sqlalchemy.engine.reflection import Inspector
from sqlalchemy.types import INTEGER, TIMESTAMP
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.testing import AsyncHTTPTestCase, gen_test
from tornado.web import Application
from tornado.websocket import websocket_connect, WebSocketHandler

from circle_core import database
from circle_core.cli.cli_main import cli_main
from circle_core.database import Database
from circle_core.models import message
from circle_core.models.message_box import MessageBox
from circle_core.models.metadata.base import MetadataReader
from circle_core.models.module import Module
from circle_core.models.schema import Schema
from circle_core.server.ws import ReplicationMaster, SensorHandler
from circle_core.workers import replication_slave
from circle_core.workers.replication_slave import ReplicationSlave


class DummyMetadata(MetadataReader):
    schemas = [Schema('95eef02e-36e5-446e-9fea-aedd10321f6f', 'json', [{'name': 'hoge', 'type': 'int'}])]
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


@pytest.mark.usefixtures('class_wide_mysql')
class TestReplicationSlave:
    @classmethod
    def setup_class(cls):
        replication_slave.get_uuid = lambda: '5c8fe778-1cb8-4a92-8f5d-588990a19def'
        replication_slave.metadata = DummyMetadata
        message.metadata = DummyMetadata
        database.metadata = DummyMetadata

    def teardown_method(self, method):
        ioloop = IOLoop.current()
        self.server.stop()
        ioloop.add_callback(ioloop.stop)
        self.thread.join()

    def run_dummy_server(self, replication_master):
        def run():
            app = Application([
                (r'/replication/(?P<slave_uuid>[0-9A-Fa-f-]+)', replication_master)
            ])
            self.server = HTTPServer(app)
            self.server.listen(5001)
            IOLoop.current().start()

        self.thread = Thread(target=run)
        self.thread.daemon = True
        self.thread.start()
        sleep(1)

    @pytest.mark.timeout(2)
    def test_migrate(self):
        DummyMetadata.database_url = self.mysql.url

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
                            'dictified_properties': [{'name': 'hoge', 'type': 'int'}]
                        }]
                    })
                    self.write_message(res)

        self.run_dummy_server(DummyReplicationMaster)

        slave = ReplicationSlave(DummyMetadata, 'localhost:5001', [])
        req = json.dumps({
            'command': 'MIGRATE'
        })
        slave.ws.send(req)
        slave.migrate()

        # Redisに同期親の情報が書き込まれているか
        assert filter(lambda schema: schema.uuid == UUID('8e654793-5c46-4721-911e-b9d19f0779f9'), DummyMetadata.schemas)
        assert filter(lambda box: box.uuid == UUID('316720eb-84fe-43b3-88b7-9aad49a93220'), DummyMetadata.message_boxes)
        assert filter(lambda module: module.uuid == UUID('8e654793-5c46-4721-911e-b9d19f0779f9'), DummyMetadata.modules)

        db = Database(self.mysql.url)
        engine = create_engine(self.mysql.url)
        inspector = Inspector.from_engine(engine)
        box = MessageBox('316720eb-84fe-43b3-88b7-9aad49a93220', '44ae2fd8-52d0-484d-9a48-128b07937a0a')
        table_name = db.make_table_name_for_message_box(box)
        columns = inspector.get_columns(table_name)
        types = {
            '_created_at': TIMESTAMP,
            '_counter': INTEGER,
            'hoge': INTEGER
        }

        # DBのテーブルが同期されているか
        for column in columns:
            assert isinstance(column['type'], types[column['name']])

    @pytest.mark.timeout(3)
    def test_receive(self):
        now = time()

        class DummyReplicationMaster(WebSocketHandler):
            def on_message(self, req):
                req = json.loads(req)
                if req['command'] == 'RECEIVE':
                    resp = json.dumps({
                        'module_uuid': '8e654793-5c46-4721-911e-b9d19f0779f9',
                        'timestamp': now,
                        'count': 0,
                        'payload': {
                            'hoge': 123
                        }
                    })
                    self.write_message(resp)
                    raise RuntimeError('This exception is used to stop DummyReplicationMaster.')

        self.run_dummy_server(DummyReplicationMaster)

        slave = ReplicationSlave(DummyMetadata, 'localhost:5001', [])
        req = json.dumps({
            'command': 'RECEIVE'
        })
        slave.ws.send(req)
        slave.receive()

        db = Database(self.mysql.url)
        table = Table('message_box_76pzhAbUqxJeYp1CYkLBc3', db._metadata, autoload=True, autoload_with=db._engine)
        session = db._session()

        # テーブルにメッセージが書き込まれているか
        with session.begin():
            rows = session.query(table).all()
            assert len(rows) == 1
            assert datetime.timestamp(rows[0]._created_at) == now
            assert rows[0]._counter == 0
            assert rows[0].hoge == 123
