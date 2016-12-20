# -*- coding: utf-8 -*-
import json
from multiprocessing import Process
from time import sleep
from uuid import UUID

import pytest
from tornado.ioloop import IOLoop
from tornado.web import Application
from websocket import create_connection

from circle_core.models.module import Module
from circle_core.models.schema import Schema
from circle_core.server import ws
from circle_core.server.ws.replication import ReplicationHandler


class DummyMetadata:
    schemas = [Schema('44ae2fd8-52d0-484d-9a48-128b07937a0a', 'DummySchema', 'hoge:int')]
    modules = [Module(
        '8e654793-5c46-4721-911e-b9d19f0779f9',
        '44ae2fd8-52d0-484d-9a48-128b07937a0a',
        'DummyModule',
        'foo:bar'
    )]

    @classmethod
    def find_module(cls, *args):
        return cls.modules[0]


def start_replication_server():
    ws.run(DummyMetadata, '/ws', 5001)


class TestReplicationHandler:
    @classmethod
    def setup_class(cls):
        cls.server = Process(target=start_replication_server)
        cls.server.start()
        sleep(0.1)
        cls.dummy_crcr = create_connection('ws://localhost:5001/ws')
        cls.dummy_module = create_connection('ws://localhost:5001/ws/8e654793-5c46-4721-911e-b9d19f0779f9')

    @classmethod
    def teardown_method(cls):
        cls.dummy_crcr.close()
        cls.dummy_module.close()
        cls.server.terminate()

    # @pytest.mark.timeout(1)
    # def test_handshake(self):
    #     self.dummy_crcr.send('{"type": "HANDSHAKE"}')
    #     resp = json.loads(self.dummy_crcr.recv())

    #     schema = Schema(**resp['schemas'][0])
    #     assert schema.uuid == UUID('44ae2fd8-52d0-484d-9a48-128b07937a0a')
    #     assert schema.display_name == 'DummySchema'
    #     assert schema.properties[0].name == 'hoge'
    #     assert schema.properties[0].type == 'int'

    #     module = Module(**resp['modules'][0])
    #     assert module.uuid == UUID('8e654793-5c46-4721-911e-b9d19f0779f9')
    #     assert module.schema_uuid == UUID('44ae2fd8-52d0-484d-9a48-128b07937a0a')
    #     assert module.display_name == 'DummyModule'
    #     assert module.properties[0].name == 'foo'
    #     assert module.properties[0].value == 'bar'

    @pytest.mark.timeout(1)
    def test_ready(self):
        # FIXME: PythonのREPLから手で打てば通るのに...
        self.dummy_crcr.send('{"type": "READY"}')
        self.dummy_module.send('{"hoge": 123}')
        assert json.loads(self.dummy_crcr.recv()) == {
            'module': '8e654793-5c46-4721-911e-b9d19f0779f9',
            'payload': {
                'hoge': 123
            }
        }
