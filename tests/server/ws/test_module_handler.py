# -*- coding: utf-8 -*-
import json
from uuid import UUID

import pytest
from tornado.gen import sleep
from tornado.testing import AsyncHTTPTestCase, gen_test
from tornado.web import Application
from tornado.websocket import websocket_connect, WebSocketClosedError

from circle_core.helpers.nanomsg import Receiver
# from circle_core.helpers.topics import ModuleMessageTopic
# from circle_core.models import message
from circle_core.models import MessageBox, Module, Schema
# from circle_core.server.ws import module
# from circle_core.server.ws import ModuleHandler


# class DummyMetadata(MetadataReader):
#     schemas = [Schema('384e637b-375f-498d-8fc2-73e5cc1e6892', 'DummySchema', [{'name': 'hoge', 'type': 'text'}])]
#     message_boxes = [
#         MessageBox(
#             'e170a8e5-3157-484e-b7d2-9816b0d97546', '384e637b-375f-498d-8fc2-73e5cc1e6892',
#             'e170a8e5-3157-484e-b7d2-9816b0d97546', 'DummyMessageBox')
#     ]
#     modules = [Module('4ffab839-cf56-478a-8614-6003a5980855', 'DummyModule')]
#     users = []
#     replication_links = []
#     cc_infos = []
#     invitations = []
#     parse_url_scheme = None


@pytest.mark.skip(reason='rewriting...')
class TestModuleHandler(AsyncHTTPTestCase):
    def get_app(self):
        return Application([
            ('/module/(?P<module_uuid>[0-9A-Fa-f-]+)', ModuleHandler)
        ])

    def get_protocol(self):
        return 'ws'

    def setUp(self):
        super().setUp()
        message.metadata = DummyMetadata
        module.metadata = DummyMetadata
        self.receiver = Receiver(ModuleMessageTopic())
        self.messages = iter(self.receiver)

    def tearDown(self):
        super().tearDown()
        del self.receiver

    @pytest.mark.timeout(2)
    @gen_test
    def test_module_not_found(self):
        """登録されていないModuleから接続された際は切断."""
        unknown_module = yield websocket_connect(
            self.get_url('/module/eaf8c6d5-1ce0-4a45-848f-9c80b0fbb2d7'),
            self.io_loop
        )
        res = yield unknown_module.read_message()
        assert res is None

    @pytest.mark.timeout(2)
    @gen_test
    def test_pass_to_nanomsg(self):
        """WebSocketで受け取ったModuleからのMessageに適切なtimestamp/countを付与してnanomsgに流せているかどうか."""
        dummy_module = yield websocket_connect(
            self.get_url('/module/4ffab839-cf56-478a-8614-6003a5980855'),
            self.io_loop
        )
        req = json.dumps({
            'hoge': 'piyo',
            '_box': 'e170a8e5-3157-484e-b7d2-9816b0d97546',
        })
        dummy_module.write_message(req)
        # 素直にrecvするとIOLoopがブロックされてModuleHandlerが何も返せなくなるのでModuleHandlerをまず動かす
        yield sleep(1)
        res = next(self.messages)
        assert res.count == 0
        assert res.module_uuid == UUID('4ffab839-cf56-478a-8614-6003a5980855')
        assert res.payload == {
            'hoge': 'piyo'
        }
