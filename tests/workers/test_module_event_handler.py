# -*- coding: utf-8 -*-
import json
from unittest.mock import MagicMock
from uuid import UUID

import pytest
from tornado.gen import sleep
from tornado.testing import AsyncHTTPTestCase, gen_test
from tornado.web import Application
from tornado.websocket import websocket_connect, WebSocketClosedError

from circle_core.models import MessageBox, MetaDataSession, Module, Schema
from circle_core.testing import setup_db
from circle_core.workers.http import ModuleEventHandler


class TestModuleEventHandlerBase(AsyncHTTPTestCase):

    def get_app(self):
        return Application(
            [
                (r'/modules/(?P<module_uuid>[0-9A-Fa-f-]+)/(?P<mbox_uuid>[0-9A-Fa-f-]+)', ModuleEventHandler),
            ],
            _core=self.app_mock
        )

    def setUp(self):
        self.app_mock = MagicMock()
        self.datareceiver = MagicMock()
        self.datareceiver.receive_new_message.return_value = None
        self.app_mock.get_datareceiver.return_value = self.datareceiver

        super().setUp()
        setup_db()


class TestModuleEventHandlerViaREST(TestModuleEventHandlerBase):

    def test_rest_not_found(self):
        """登録されていないModuleからのPOSTは404"""
        response = self.fetch(
            self.get_url('/modules/4ffab839-cf56-478a-8614-6003a5980855/00000000-0000-0000-0000-000000000000'),
            method='POST',
            body=json.dumps({
                'x': 1,
                'y': 2
            }),
            headers={'Content-Type': 'application/json'}
        )
        self.assertEqual(response.code, 404)

    def test_rest(self):
        """登録されているModuleからのPOSTは404"""
        # make dummy environ
        with MetaDataSession.begin():
            schema = Schema.create(display_name='Schema', properties='x:int,y:float')
            module = Module.create(display_name='Module')
            mbox = MessageBox(
                uuid='4ffab839-cf56-478a-8614-6003a5980856', schema_uuid=schema.uuid, module_uuid=module.uuid
            )
            MetaDataSession.add(schema)
            MetaDataSession.add(module)
            MetaDataSession.add(mbox)

        print(self.get_url('/modules/{}/{}'.format(module.uuid, mbox.uuid)))
        response = self.fetch(
            self.get_url('/modules/{}/{}'.format(module.uuid, mbox.uuid)),
            method='POST',
            body=json.dumps({
                'x': 1,
                'y': 2.5
            }),
            headers={'Content-Type': 'application/json'}
        )
        self.assertEqual(response.code, 200)
        self.datareceiver.receive_new_message.assert_called_once_with(str(mbox.uuid), {'x': 1, 'y': 2.5})


class TestModuleEventHandlerViaWebsocket(TestModuleEventHandlerBase):

    def get_protocol(self):
        return 'ws'

    @gen_test(timeout=2)
    def test_websocket_not_found(self):
        """登録されていないModuleから接続された際は切断."""
        unknown_box = yield websocket_connect(
            self.get_url('/modules/4ffab839-cf56-478a-8614-6003a5980855/00000000-0000-0000-0000-000000000000')
        )
        res = yield unknown_box.read_message()
        assert res is None

    @gen_test(timeout=2)
    def test_websocket_pass_to_nanomsg(self):
        """WebSocketで受け取ったModuleからのMessageに適切なtimestamp/countを付与してnanomsgに流せているかどうか."""

        # make dummy environ
        schema = Schema.create(display_name='Schema', properties='x:int,y:float')
        module = Module.create(display_name='Module')
        mbox = MessageBox(uuid='4ffab839-cf56-478a-8614-6003a5980855', schema_uuid=schema.uuid, module_uuid=module.uuid)

        with MetaDataSession.begin():
            MetaDataSession.add(schema)
            MetaDataSession.add(module)
            MetaDataSession.add(mbox)

        dummy_module = yield websocket_connect(self.get_url('/modules/{}/{}'.format(module.uuid, mbox.uuid)))
        dummy_module.write_message(json.dumps({'x': 1, 'y': 2}))

        # 素直にrecvするとIOLoopがブロックされてModuleHandlerが何も返せなくなるのでModuleHandlerをまず動かす
        yield sleep(1)
        self.datareceiver.receive_new_message.assert_called_once_with(
            '4ffab839-cf56-478a-8614-6003a5980855', {
                'x': 1,
                'y': 2
            }
        )
