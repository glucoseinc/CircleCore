# -*- coding: utf-8 -*-
import json
from uuid import UUID

import pytest
from tornado.gen import sleep
from tornado.testing import AsyncHTTPTestCase, gen_test
from tornado.web import Application
from tornado.websocket import websocket_connect

from circle_core.helpers.nanomsg import Receiver
from circle_core.helpers.topics import ModuleMessageTopic
from circle_core.models import message
from circle_core.models.message_box import MessageBox
from circle_core.models.metadata.base import MetadataReader
from circle_core.models.module import Module
from circle_core.models.schema import Schema
from circle_core.server.ws import ModuleHandler


class DummyMetadata(MetadataReader):
    schemas = [Schema('384e637b-375f-498d-8fc2-73e5cc1e6892', 'DummySchema', [{'name': 'hoge', 'type': 'text'}])]
    message_boxes = [MessageBox('e170a8e5-3157-484e-b7d2-9816b0d97546', '384e637b-375f-498d-8fc2-73e5cc1e6892')]
    modules = [Module('4ffab839-cf56-478a-8614-6003a5980855', 'e170a8e5-3157-484e-b7d2-9816b0d97546', 'DummyModule')]
    users = []
    parse_url_scheme = None


class TestModuleHandler(AsyncHTTPTestCase):
    def get_app(self):
        return Application([
            ('/ws/(?P<module_uuid>[0-9A-Fa-f-]+)', ModuleHandler)
        ], cr_metadata=DummyMetadata())

    def get_protocol(self):
        return 'ws'

    def setUp(self):
        super().setUp()
        message.metadata = DummyMetadata
        self.receiver = Receiver(ModuleMessageTopic())
        self.messages = self.receiver.incoming_messages()

    def tearDown(self):
        super().tearDown()
        del self.receiver

    @pytest.mark.timeout(2)
    @gen_test
    def test_pass_to_nanomsg(self):
        """WebSocketで受け取ったModuleからのMessageに適切なtimestamp/countを付与してnanomsgに流せているかどうか."""
        dummy_module = yield websocket_connect(self.get_url('/ws/4ffab839-cf56-478a-8614-6003a5980855'), self.io_loop)
        req = json.dumps({
            'hoge': 'piyo'
        })
        dummy_module.write_message(req)
        # 素直にrecvするとIOLoopがブロックされてModuleHandlerが何も返せなくなるのでModuleHandlerをまず動かす
        yield sleep(1)
        res = next(self.messages)
        assert res.count == 0
        assert res.module.uuid == UUID('4ffab839-cf56-478a-8614-6003a5980855')
        assert res.payload == {
            'hoge': 'piyo'
        }
