# -*- coding: utf-8 -*-
from datetime import datetime
import json
from time import time
from uuid import UUID

import pytest
from tornado.gen import coroutine, sleep
from tornado.testing import AsyncHTTPTestCase, gen_test
from tornado.web import Application
from tornado.websocket import websocket_connect

from circle_core.database import Database
from circle_core.models import message
from circle_core.models import message_box
from circle_core.models.message_box import MessageBox
from circle_core.models.metadata.base import MetadataReader
from circle_core.models.module import Module
from circle_core.models.schema import Schema
from circle_core.server.ws import replication_master
from circle_core.server.ws import ReplicationMaster, SensorHandler


class DummyMetadata(MetadataReader):
    schemas = [Schema('44ae2fd8-52d0-484d-9a48-128b07937a0a', 'DummySchema', [{'name': 'hoge', 'type': 'int'}])]
    message_boxes = [MessageBox('316720eb-84fe-43b3-88b7-9aad49a93220', '44ae2fd8-52d0-484d-9a48-128b07937a0a')]
    modules = [Module(
        '8e654793-5c46-4721-911e-b9d19f0779f9',
        '316720eb-84fe-43b3-88b7-9aad49a93220',
        'DummyModule',
        'foo,bar'
    )]
    users = []
    parse_url_scheme = None


@pytest.mark.usefixtures('class_wide_mysql')
class TestReplicationMaster(AsyncHTTPTestCase):
    def get_app(self):
        return Application([
            ('/replication/(?P<slave_uuid>[0-9A-Fa-f-]+)', ReplicationMaster),
            ('/ws/(?P<module_uuid>[0-9A-Fa-f-]+)', SensorHandler)
        ], cr_metadata=DummyMetadata())

    def get_protocol(self):
        return 'ws'

    def setUp(self):
        super(TestReplicationMaster, self).setUp()
        message.metadata = DummyMetadata
        replication_master.metadata = DummyMetadata
        message_box.metadata = DummyMetadata

        @coroutine
        def connect():
            self.dummy_crcr = yield websocket_connect(
                self.get_url('/replication/d267f765-8a72-4056-94b3-7b1a63f47da6'),
                self.io_loop
            )
            self.dummy_module = yield websocket_connect(
                self.get_url('/ws/8e654793-5c46-4721-911e-b9d19f0779f9'),
                self.io_loop
            )

        self.io_loop.run_sync(connect)

    def tearDown(self):
        self.dummy_crcr.close()
        self.dummy_module.close()
        super(TestReplicationMaster, self).tearDown()

    @pytest.mark.timeout(2)
    @gen_test
    def test_migrate(self):
        """レプリケーション親が自身に登録されているModule/MessageBox/Schemaをすべて返すか

        TODO: レプリケーション親がまた別のCircleCoreのレプリケーション子になっていた場合、それらの情報は除く
        """
        yield self.dummy_crcr.write_message('{"command": "MIGRATE"}')
        resp = yield self.dummy_crcr.read_message()
        resp = json.loads(resp)

        schema = Schema(**resp['schemas'][0])
        assert schema.uuid == UUID('44ae2fd8-52d0-484d-9a48-128b07937a0a')
        assert schema.display_name == 'DummySchema'
        assert schema.properties[0].name == 'hoge'
        assert schema.properties[0].type == 'int'

        box = MessageBox(**resp['message_boxes'][0])
        assert box.uuid == UUID('316720eb-84fe-43b3-88b7-9aad49a93220')
        assert box.schema_uuid == UUID('44ae2fd8-52d0-484d-9a48-128b07937a0a')

        module = Module(**resp['modules'][0])
        assert module.uuid == UUID('8e654793-5c46-4721-911e-b9d19f0779f9')
        assert module.message_box_uuids[0] == UUID('316720eb-84fe-43b3-88b7-9aad49a93220')
        assert module.display_name == 'DummyModule'
        assert module.tags == ['foo', 'bar']

    @pytest.mark.timeout(2)
    @gen_test
    def test_receive(self):
        """新着メッセージがレプリケーション子にたらい回せているか"""
        yield self.dummy_crcr.write_message('{"command": "RECEIVE", "payload": {}}')
        yield sleep(1)
        yield self.dummy_module.write_message('{"hoge": 123}')
        resp = yield self.dummy_crcr.read_message()
        resp = json.loads(resp)
        assert resp['count'] == 0
        assert resp['module_uuid'] == UUID('8e654793-5c46-4721-911e-b9d19f0779f9').hex
        assert resp['payload'] == {
            'hoge': 123
        }

    @pytest.mark.timeout(120)  # 遅い...
    @gen_test
    def test_receive_count(self):
        # setUpとtearDownはメソッド毎に実行されてる？
        yield self.dummy_crcr.write_message('{"command": "RECEIVE", "payload": {}}')
        yield sleep(1)

        # カウントの増加
        for i in range(1, 32768):
            yield self.dummy_module.write_message('{"hoge": 678}')
            resp = yield self.dummy_crcr.read_message()
            assert json.loads(resp)['count'] == i

        # カウントのリセット
        yield self.dummy_module.write_message('{"hoge": 45}')
        resp = yield self.dummy_crcr.read_message()
        assert json.loads(resp)['count'] == 0

    @pytest.mark.timeout(2)
    @gen_test
    def test_receive_count_seeding(self):  # メソッド名で実行順が決まってる？
        DummyMetadata.database_url = self.mysql.url
        now = round(time(), 6)

        # timestampが同じでcountが違う場合
        db = Database(self.mysql.url)
        db.register_message_boxes(DummyMetadata.message_boxes, DummyMetadata.schemas)
        db.migrate()
        table = db.find_table_for_message_box(DummyMetadata.message_boxes[0])
        db._engine.execute(table.insert(), _created_at=datetime.fromtimestamp(now), _counter=0, hoge=123)
        db._engine.execute(table.insert(), _created_at=datetime.fromtimestamp(now), _counter=1, hoge=678)

        req = json.dumps({
            'command': 'RECEIVE',
            'payload': {
                '316720eb-84fe-43b3-88b7-9aad49a93220': {
                    'timestamp': now,
                    'count': 0
                }
            }
        })
        yield self.dummy_crcr.write_message(req)
        resp = yield self.dummy_crcr.read_message()
        resp = json.loads(resp)
        assert resp['timestamp'] == now
        assert resp['count'] == 1
        assert UUID(resp['module_uuid']) == UUID('8e654793-5c46-4721-911e-b9d19f0779f9')
        assert resp['payload'] == {'hoge': 678}

        # countが同じでtimestampが違う場合
        now = time()
        db._engine.execute(table.insert(), _created_at=datetime.fromtimestamp(now - 0.000001), _counter=0, hoge=234)
        db._engine.execute(table.insert(), _created_at=datetime.fromtimestamp(now), _counter=0, hoge=789)

        req = json.dumps({
            'command': 'RECEIVE',
            'payload': {
                '316720eb-84fe-43b3-88b7-9aad49a93220': {
                    'timestamp': now - 0.000001,
                    'count': 0
                }
            }
        })
        yield self.dummy_crcr.write_message(req)
        resp = yield self.dummy_crcr.read_message()
        resp = json.loads(resp)
        assert resp['timestamp'] == now
        assert resp['count'] == 0
        assert UUID(resp['module_uuid']) == UUID('8e654793-5c46-4721-911e-b9d19f0779f9')
        assert resp['payload'] == {'hoge': 789}

        # countもtimestampも違う場合
        now = time()
        db._engine.execute(table.insert(), _created_at=datetime.fromtimestamp(now - 0.000001), _counter=1, hoge=345)
        db._engine.execute(table.insert(), _created_at=datetime.fromtimestamp(now), _counter=0, hoge=543)

        req = json.dumps({
            'command': 'RECEIVE',
            'payload': {
                '316720eb-84fe-43b3-88b7-9aad49a93220': {
                    'timestamp': now - 0.000001,
                    'count': 1
                }
            }
        })
        yield self.dummy_crcr.write_message(req)
        resp = yield self.dummy_crcr.read_message()
        resp = json.loads(resp)
        assert resp['timestamp'] == now
        assert resp['count'] == 0
        assert UUID(resp['module_uuid']) == UUID('8e654793-5c46-4721-911e-b9d19f0779f9')
        assert resp['payload'] == {'hoge': 543}
