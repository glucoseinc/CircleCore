
# -*- coding: utf-8 -*-
import json
from uuid import UUID

import pytest
from tornado.gen import coroutine, sleep
from tornado.testing import AsyncHTTPTestCase, gen_test
from tornado.web import Application
from tornado.websocket import websocket_connect

from circle_core.models import message
from circle_core.models.message_box import MessageBox
from circle_core.models.metadata.base import MetadataReader
from circle_core.models.module import Module
from circle_core.models.schema import Schema
from circle_core.server.ws import ReplicationHandler, SensorHandler


class DummyMetadata(MetadataReader):
    schemas = [Schema('44ae2fd8-52d0-484d-9a48-128b07937a0a', 'DummySchema', 'hoge:int')]
    message_boxes = [MessageBox('316720eb-84fe-43b3-88b7-9aad49a93220', '44ae2fd8-52d0-484d-9a48-128b07937a0a')]
    modules = [Module(
        '8e654793-5c46-4721-911e-b9d19f0779f9',
        '316720eb-84fe-43b3-88b7-9aad49a93220',
        'DummyModule',
        'foo,bar'
    )]
    users = []
    parse_url_scheme = None


class TestReplicationHandler(AsyncHTTPTestCase):
    def get_app(self):
        return Application([
            ('/replication/(?P<slave_uuid>[0-9A-Fa-f-]+)', ReplicationHandler),
            ('/ws/(?P<module_uuid>[0-9A-Fa-f-]+)', SensorHandler)
        ], cr_metadata=DummyMetadata())

    def get_protocol(self):
        return 'ws'

    def setUp(self):
        super(TestReplicationHandler, self).setUp()
        message.metadata = DummyMetadata

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
        super(TestReplicationHandler, self).tearDown()

    @pytest.mark.timeout(2)
    @gen_test
    def test_migrate(self):
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
        yield self.dummy_crcr.write_message('{"command": "RECEIVE"}')
        yield sleep(1)
        yield self.dummy_module.write_message('{"hoge": 123}')
        resp = yield self.dummy_crcr.read_message()
        resp = json.loads(resp)
        assert resp['module'] == UUID('8e654793-5c46-4721-911e-b9d19f0779f9').hex
        assert resp['payload'] == {
            'hoge': 123
        }
