# -*- coding: utf-8 -*-
from datetime import datetime
import json
from multiprocessing import Process
from threading import Thread
from time import time
from uuid import UUID

import pytest
from tornado.gen import coroutine, sleep
from tornado.testing import AsyncHTTPTestCase, gen_test
from tornado.web import Application
from tornado.websocket import websocket_connect, WebSocketHandler

from circle_core.database import Database
from circle_core.models import message
from circle_core.models import message_box
from circle_core.models import module
from circle_core.models import schema
from circle_core.models.message import ModuleMessage
from circle_core.models.message_box import MessageBox
from circle_core.models.metadata.base import MetadataReader
from circle_core.models.module import Module
from circle_core.models.schema import Schema
from circle_core.server.ws import module as module_handler, replication_master
from circle_core.server.ws import ModuleHandler, ReplicationMaster
from circle_core.workers import replication_slave
from circle_core.workers.replication_slave import ReplicationSlave


class DummyMetadata(MetadataReader):
    schemas = [
        Schema('44ae2fd8-52d0-484d-9a48-128b07937a0a', 'DummySchema', [{'name': 'hoge', 'type': 'int'}]),
        Schema('17be0dbf-73c2-4055-9aa9-2a487dd8475b', 'DummySchema2', [{'name': 'piyo', 'type': 'float'}])
    ]
    message_boxes = [
        MessageBox('316720eb-84fe-43b3-88b7-9aad49a93220', '44ae2fd8-52d0-484d-9a48-128b07937a0a', 'DummyMessageBox1'),
        MessageBox('3d5a6cc9-d496-4858-8541-ce0d9673422e', '17be0dbf-73c2-4055-9aa9-2a487dd8475b', 'DummyMessageBox2')
    ]
    modules = [Module(
        '8e654793-5c46-4721-911e-b9d19f0779f9',
        ['316720eb-84fe-43b3-88b7-9aad49a93220'],
        'DummyModule',
        'foo,bar'
    ), Module(
        'a1956117-bf4e-4ddb-b840-5cd3d9708b49',
        ['3d5a6cc9-d496-4858-8541-ce0d9673422e'],
        'DummyModule2',
        'fooo,baar'
    )]
    invitations = []
    users = []
    replication_links = []
    parse_url_scheme = None
    writable = True

    def register_schema(self, schema):
        self.schemas.append(schema)

    def register_message_box(self, box):
        self.message_boxes.append(box)

    def register_module(self, module):
        self.modules.append(module)


class DummyReplicationMaster(WebSocketHandler):
    def on_message(self, plain_msg):
        json_msg = json.loads(plain_msg)
        if json_msg['command'] == 'MIGRATE':
            res = json.dumps({
                'crcr_uuid': '61b55e35-d769-429f-a464-9efe14a2d573',
                'schemas': [Schema(
                    '3038b66a-9ebd-4f1b-8ca6-6281e004bb76',
                    'DummySchema',
                    [{'name': 'hoge', 'type': 'text'}]
                ).to_json()],
                'message_boxes': [MessageBox(
                    '9168d87f-72cc-4dff-90d5-ad30e3e28958',
                    '3038b66a-9ebd-4f1b-8ca6-6281e004bb76',
                    'DummyBox'
                ).to_json()],
                'modules': [Module(
                    'f0c5da15-d1f3-43b9-bbc0-423a6d5bcd8f',
                    ['9168d87f-72cc-4dff-90d5-ad30e3e28958'],
                    'DummyModule'
                ).to_json()]
            })
            self.write_message(res)


@pytest.mark.usefixtures('class_wide_mysql')
class TestReplicationMaster(AsyncHTTPTestCase):
    def get_app(self):
        return Application([
            ('/replication/', DummyReplicationMaster),
            ('/replication/(?P<slave_uuid>[0-9A-Fa-f-]+)', ReplicationMaster),
            ('/module/(?P<module_uuid>[0-9A-Fa-f-]+)', ModuleHandler)
        ])

    def get_protocol(self):
        return 'ws'

    def setUp(self):
        super(TestReplicationMaster, self).setUp()
        # 汚い...
        schema.metadata = DummyMetadata
        module.metadata = DummyMetadata
        message.metadata = DummyMetadata
        replication_master.metadata = DummyMetadata
        replication_slave.metadata = DummyMetadata
        message_box.metadata = DummyMetadata
        module_handler.metadata = DummyMetadata

        @coroutine
        def connect():
            self.dummy_crcr = yield websocket_connect(
                self.get_url('/replication/d267f765-8a72-4056-94b3-7b1a63f47da6'),
                self.io_loop
            )
            self.dummy_module = yield websocket_connect(
                self.get_url('/module/8e654793-5c46-4721-911e-b9d19f0779f9'),
                self.io_loop
            )

        self.io_loop.run_sync(connect)

    @pytest.mark.timeout(2)
    @gen_test
    def test_migrate(self):
        """レプリケーション親が指定されたModule及びそれに関連するSchema/MessageBoxを返すかどうか"""
        req = json.dumps({
            'command': 'MIGRATE',
            'module_uuids': ['8e654793-5c46-4721-911e-b9d19f0779f9']
        })
        yield self.dummy_crcr.write_message(req)
        resp = yield self.dummy_crcr.read_message()
        resp = json.loads(resp)

        schema = Schema.from_json(resp['schemas'][0])
        assert schema.uuid == UUID('44ae2fd8-52d0-484d-9a48-128b07937a0a')
        assert schema.display_name == 'DummySchema'
        assert schema.properties[0].name == 'hoge'
        assert schema.properties[0].type == 'int'

        box = MessageBox.from_json(resp['message_boxes'][0])
        assert box.uuid == UUID('316720eb-84fe-43b3-88b7-9aad49a93220')
        assert box.schema_uuid == UUID('44ae2fd8-52d0-484d-9a48-128b07937a0a')

        module = Module.from_json(resp['modules'][0])
        assert module.uuid == UUID('8e654793-5c46-4721-911e-b9d19f0779f9')
        assert module.message_box_uuids[0] == UUID('316720eb-84fe-43b3-88b7-9aad49a93220')
        assert module.display_name == 'DummyModule'
        assert module.tags == ['foo', 'bar']

    @pytest.mark.timeout(2)
    @gen_test
    def test_receive(self):
        """新着メッセージがレプリケーション子にたらい回せているか"""
        req = json.dumps({
            'command': 'MIGRATE',
            'module_uuids': ['8e654793-5c46-4721-911e-b9d19f0779f9']
        })
        yield self.dummy_crcr.write_message(req)
        yield self.dummy_crcr.read_message()
        yield self.dummy_crcr.write_message('{"command": "RECEIVE", "payload": {}}')
        yield sleep(1)

        # MIGRATE時に要求しなかったのでたらい回されない
        dummy_module2 = yield websocket_connect(
            self.get_url('/module/a1956117-bf4e-4ddb-b840-5cd3d9708b49'),
            self.io_loop
        )
        yield dummy_module2.write_message('{"piyo": 12.3, "_box": "17be0dbf-73c2-4055-9aa9-2a487dd8475b"}')

        # MIGRATE時に要求したのでたらい回される
        yield self.dummy_module.write_message('{"hoge": 123, "_box": "316720eb-84fe-43b3-88b7-9aad49a93220"}')
        resp = yield self.dummy_crcr.read_message()
        resp = json.loads(resp)
        assert resp['count'] == 0
        assert resp['module_uuid'] == UUID('8e654793-5c46-4721-911e-b9d19f0779f9').hex
        assert resp['payload'] == {
            'hoge': 123
        }

    @pytest.mark.skip
    @pytest.mark.timeout(120)  # 遅い...
    @gen_test
    def test_receive_count(self):
        # setUpとtearDownはメソッド毎に実行されてる？
        req = json.dumps({
            'command': 'MIGRATE',
            'module_uuids': ['8e654793-5c46-4721-911e-b9d19f0779f9']
        })
        yield self.dummy_crcr.write_message(req)
        yield self.dummy_crcr.read_message()
        yield self.dummy_crcr.write_message('{"command": "RECEIVE", "payload": {}}')
        yield sleep(1)

        # カウントの増加
        for i in range(1, 32768):
            yield self.dummy_module.write_message('{"hoge": 678, "_box": "316720eb-84fe-43b3-88b7-9aad49a93220"}')
            resp = yield self.dummy_crcr.read_message()
            assert json.loads(resp)['count'] == i

        # 32767を超えたので、カウントのリセット
        yield self.dummy_module.write_message('{"hoge": 45, "_box": "316720eb-84fe-43b3-88b7-9aad49a93220"}')
        resp = yield self.dummy_crcr.read_message()
        assert json.loads(resp)['count'] == 0

    @pytest.mark.timeout(2)
    @gen_test
    def test_receive_count_seeding(self):  # メソッド名で実行順が決まってる？
        """過去に蓄えたデータの送信。

        指定した時点以降のデータのみ送られてくるか。
        """
        DummyMetadata.database_url = self.mysql.url
        now = ModuleMessage.make_timestamp(time())

        # timestampが同じでcountが違う場合
        db = Database(self.mysql.url)
        db.register_message_boxes(DummyMetadata.message_boxes, DummyMetadata.schemas)
        db.migrate()
        table = db.find_table_for_message_box(DummyMetadata.message_boxes[0])
        db._engine.execute(table.insert(), _created_at=now, _counter=0, hoge=123)
        db._engine.execute(table.insert(), _created_at=now, _counter=1, hoge=678)

        req = json.dumps({
            'command': 'RECEIVE',
            'payload': {
                '316720eb-84fe-43b3-88b7-9aad49a93220': {
                    'timestamp': str(now),
                    'count': 0
                }
            }
        })
        yield self.dummy_crcr.write_message(req)
        resp = yield self.dummy_crcr.read_message()
        resp = json.loads(resp)

        assert ModuleMessage.is_equal_timestamp(resp['timestamp'], now)
        assert resp['count'] == 1
        assert UUID(resp['module_uuid']) == UUID('8e654793-5c46-4721-911e-b9d19f0779f9')
        assert resp['payload'] == {'hoge': 678}

        # countが同じでtimestampが違う場合
        past = now + 1
        now = now + 2
        db._engine.execute(table.insert(), _created_at=past, _counter=0, hoge=234)
        db._engine.execute(table.insert(), _created_at=now, _counter=0, hoge=789)

        req = json.dumps({
            'command': 'RECEIVE',
            'payload': {
                '316720eb-84fe-43b3-88b7-9aad49a93220': {
                    'timestamp': str(past),
                    'count': 0
                }
            }
        })
        yield self.dummy_crcr.write_message(req)
        resp = yield self.dummy_crcr.read_message()
        resp = json.loads(resp)

        assert ModuleMessage.is_equal_timestamp(resp['timestamp'], now)
        assert resp['count'] == 0
        assert UUID(resp['module_uuid']) == UUID('8e654793-5c46-4721-911e-b9d19f0779f9')
        assert resp['payload'] == {'hoge': 789}

        # countもtimestampも違う場合
        past = now + 1
        now = now + 2
        db._engine.execute(table.insert(), _created_at=past, _counter=1, hoge=345)
        db._engine.execute(table.insert(), _created_at=now, _counter=0, hoge=543)

        req = json.dumps({
            'command': 'RECEIVE',
            'payload': {
                '316720eb-84fe-43b3-88b7-9aad49a93220': {
                    'timestamp': str(past),
                    'count': 1
                }
            }
        })
        yield self.dummy_crcr.write_message(req)
        resp = yield self.dummy_crcr.read_message()
        resp = json.loads(resp)

        assert ModuleMessage.is_equal_timestamp(resp['timestamp'], now)
        assert resp['count'] == 0
        assert UUID(resp['module_uuid']) == UUID('8e654793-5c46-4721-911e-b9d19f0779f9')
        assert resp['payload'] == {'hoge': 543}

    @pytest.mark.timeout(2)
    @gen_test
    def test_receive_count_seeding_chain(self):
        """CircleCoreに別のCircleCoreから同期されたModule/MessageBox/Schemaが保存されていた場合に
        それをまた別のCircleCoreと同期しない"""
        def start_dummy_slave():
            replication_slave.get_uuid = lambda: ''
            slave = ReplicationSlave(
                DummyMetadata,
                'localhost:%s' % self.get_http_port(),
                ['f0c5da15-d1f3-43b9-bbc0-423a6d5bcd8f']
            )
            req = json.dumps({
                'command': 'MIGRATE'
            })
            # 中でDummyReplicationMasterにアクセスしようとするが
            # その間IOLoopがブロックされてDummyReplicationMasterが何も返せなくなるので別スレッドで
            slave.ws.send(req)
            slave.migrate()

        Thread(target=start_dummy_slave).start()
        yield sleep(1)

        req = json.dumps({
            'command': 'MIGRATE',
            'module_uuids': ['8e654793-5c46-4721-911e-b9d19f0779f9', 'f0c5da15-d1f3-43b9-bbc0-423a6d5bcd8f']
        })
        yield self.dummy_crcr.write_message(req)
        res = yield self.dummy_crcr.read_message()
        res = json.loads(res)

        assert not any(
            UUID(schema['uuid']) == UUID('3038b66a-9ebd-4f1b-8ca6-6281e004bb76')
            for schema in res['schemas']
        )
        assert not any(
            UUID(box['uuid']) == UUID('9168d87f-72cc-4dff-90d5-ad30e3e28958')
            for box in res['message_boxes']
        )
        assert not any(
            UUID(module['uuid']) == UUID('f0c5da15-d1f3-43b9-bbc0-423a6d5bcd8f')
            for module in res['modules']
        )
