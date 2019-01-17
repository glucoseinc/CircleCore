# -*- coding: utf-8 -*-
import base64
import json
import mimetypes
import os
from email.message import EmailMessage
from unittest.mock import MagicMock

from tornado import httpclient
from tornado.gen import sleep
from tornado.testing import AsyncHTTPTestCase, gen_test
from tornado.web import Application
from tornado.websocket import websocket_connect

from circle_core.models import MessageBox, MetaDataSession, Module, Schema, User
from circle_core.testing import mock_circlecore_context
from circle_core.workers.http import ModuleEventHandler


async def _receive_new_message_side_effect(*args, **kwargs):
    return True


class TestModuleEventHandlerBase(AsyncHTTPTestCase):

    def get_app(self):
        return Application(
            [(r'/modules/(?P<module_uuid>[0-9A-Fa-f-]+)/(?P<mbox_uuid>[0-9A-Fa-f-]+)', ModuleEventHandler)],
            _core=self.app_mock
        )

    def setUp(self):
        self.app_mock = MagicMock()
        self.datareceiver = MagicMock()
        self.datareceiver.receive_new_message.return_value = True
        self.datareceiver.receive_new_message.side_effect = _receive_new_message_side_effect
        self.app_mock.get_datareceiver.return_value = self.datareceiver

        super().setUp()

        self.ctxt = mock_circlecore_context()
        self.ctxt.__enter__()

    def tearDown(self):
        self.ctxt.__exit__(None, None, None)

        super().tearDown()

    def reset_mock(self):
        self.datareceiver.reset_mock()
        self.datareceiver.receive_new_message.side_effect = _receive_new_message_side_effect


class TestModuleEventHandlerViaREST(TestModuleEventHandlerBase):

    def test_rest_not_found(self):
        """登録されていないModuleからのPOSTは404"""
        with MetaDataSession.begin():
            user = User.create(account='tester', password='tester')
            user.renew_token()

            MetaDataSession.add(user)

        response = self.fetch(
            self.get_url('/modules/4ffab839-cf56-478a-8614-6003a5980855/00000000-0000-0000-0000-000000000000'),
            method='POST',
            body=json.dumps({
                'x': 1,
                'y': 2
            }),
            headers={
                'Content-Type': 'application/json',
                'Authorization': 'Bearer {token}'.format(token=user.encoded_token),
            }
        )
        self.assertEqual(response.code, 404)

    def test_rest(self):
        """登録されているModuleからのPOSTは404"""
        # make dummy environ
        with MetaDataSession.begin():
            user = User.create(account='tester', password='tester')
            user.renew_token()
            schema = Schema.create(display_name='Schema', properties='x:int,y:float')
            module = Module.create(display_name='Module')
            mbox = MessageBox(
                uuid='4ffab839-cf56-478a-8614-6003a5980856', schema_uuid=schema.uuid, module_uuid=module.uuid
            )
            MetaDataSession.add(user)
            MetaDataSession.add(schema)
            MetaDataSession.add(module)
            MetaDataSession.add(mbox)

        response = self.fetch(
            self.get_url('/modules/{}/{}'.format(module.uuid, mbox.uuid)),
            method='POST',
            body=json.dumps({
                'x': 1,
                'y': 2.5
            }),
            headers={
                'Content-Type': 'application/json',
                'Authorization': 'Bearer {token}'.format(token=user.encoded_token),
            }
        )
        self.assertEqual(response.code, 200)
        self.datareceiver.receive_new_message.assert_called_once_with(str(mbox.uuid), {'x': 1, 'y': 2.5})

    def test_rest_with_data(self):
        """登録されているModuleからのPOSTは404"""
        # make dummy environ
        with MetaDataSession.begin():
            user = User.create(account='tester', password='tester')
            user.renew_token()
            schema = Schema.create(display_name='Schema', properties='x:int,y:float,data:blob')
            module = Module.create(display_name='Module')
            mbox = MessageBox(
                uuid='4ffab839-cf56-478a-8614-6003a5980857', schema_uuid=schema.uuid, module_uuid=module.uuid
            )
            MetaDataSession.add(user)
            MetaDataSession.add(schema)
            MetaDataSession.add(module)
            MetaDataSession.add(mbox)

        async def _async_side_effect():
            print('_async_side_effect')
            return True

        # data encodingはOK
        response = self.fetch(
            self.get_url('/modules/{}/{}'.format(module.uuid, mbox.uuid)),
            method='POST',
            body=json.dumps({
                'x': 10.,
                'y': 20.5,
                'data': encode_to_data(*load_file('test.jpg'))
            }),
            headers={
                'Content-Type': 'application/json',
                'Authorization': 'Bearer {token}'.format(token=user.encoded_token),
            }
        )
        self.assertEqual(response.code, 200)
        self.datareceiver.receive_new_message.assert_called_once()
        args, kwargs = self.datareceiver.receive_new_message.call_args
        assert args[0] == str(mbox.uuid)
        assert args[1]['x'] == 10.
        assert args[1]['y'] == 20.5
        assert args[1]['data'].startswith('data:image/jpeg;')

        self.reset_mock()

        # そうじゃないのはNG
        response = self.fetch(
            self.get_url('/modules/{}/{}'.format(module.uuid, mbox.uuid)),
            method='POST',
            body=json.dumps({
                'x': 10.,
                'y': 20.5,
                'data': 'hogehoge'
            }),
            headers={
                'Content-Type': 'application/json',
                'Authorization': 'Bearer {token}'.format(token=user.encoded_token),
            }
        )
        self.assertEqual(response.code, 400)
        self.datareceiver.receive_new_message.assert_not_called()

        self.reset_mock()

        # multipartもOK
        body, headers = make_multipart_request(
            'application/json', json.dumps({
                'x': 10.,
                'y': 20.5,
                'data': 'file:///test.jpg'
            }), 'test.jpg'
        )
        headers['Authorization'] = 'Bearer {token}'.format(token=user.encoded_token)
        response = self.fetch(
            self.get_url('/modules/{}/{}'.format(module.uuid, mbox.uuid)),
            method='POST',
            headers=headers,
            body=body,
        )
        self.assertEqual(response.code, 200)
        args, kwargs = self.datareceiver.receive_new_message.call_args
        assert args[0] == str(mbox.uuid)
        assert args[1]['x'] == 10.
        assert args[1]['y'] == 20.5
        assert 'data' in args[1]


def load_file(filename):
    path = os.path.join(os.path.split(__file__)[0], filename)

    type, encoding = mimetypes.guess_type(path)

    with open(path, 'rb') as fp:
        data = fp.read()

    return type, encoding, data


def encode_to_data(content_type, encoding, data):
    return 'data:{content_type}{charset};bsae64,{encoded}'.format(
        content_type=content_type,
        charset=';charset={}'.format(encoding) if encoding else '',
        encoded=base64.b64encode(data).decode('utf-8')
    )


def make_multipart_request(content_type, mainbody, append_filename):
    message = EmailMessage()

    maintype, subtype = content_type.split('/')
    message.set_content(mainbody.encode('utf-8'), maintype=maintype, subtype=subtype)

    ct, enc, data = load_file(append_filename)
    maintype, subtype = ct.split('/')
    message.add_attachment(data, maintype=maintype, subtype=subtype, filename=append_filename)

    headerlines, body = message.as_string().split('\n\n', 1)
    headers = {}
    for ln in headerlines.split('\n'):
        k, v = ln.split(':', 1)
        headers[k] = v.lstrip()

    return body, headers


class TestModuleEventHandlerViaWebsocket(TestModuleEventHandlerBase):

    def get_protocol(self):
        return 'ws'

    @gen_test(timeout=2)
    def test_websocket_auth_failed(self):
        """Websocketにも認証がいる"""
        # make dummy environ
        with MetaDataSession.begin():
            schema = Schema.create(display_name='Schema', properties='x:int,y:float')
            module = Module.create(display_name='Module')
            mbox = MessageBox(
                uuid='4ffab839-cf56-478a-8614-6003a5980855', schema_uuid=schema.uuid, module_uuid=module.uuid
            )

            MetaDataSession.add(schema)
            MetaDataSession.add(module)
            MetaDataSession.add(mbox)

        with self.assertRaises(httpclient.HTTPClientError):
            dummy_module = yield websocket_connect(self.get_url('/modules/{}/{}'.format(module.uuid, mbox.uuid)))
            dummy_module.write_message(json.dumps({'x': 1, 'y': 2}))
            yield sleep(1)
            self.datareceiver.receive_new_message.assert_not_called()

    @gen_test(timeout=2)
    def test_websocket_not_found(self):
        """登録されていないModuleから接続された際は切断."""
        with MetaDataSession.begin():
            user = User.create(account='tester', password='tester')
            user.renew_token()

        unknown_box = yield websocket_connect(
            httpclient.HTTPRequest(
                self.get_url('/modules/4ffab839-cf56-478a-8614-6003a5980855/00000000-0000-0000-0000-000000000000'),
                headers={
                    'Authorization': 'Bearer {token}'.format(token=user.encoded_token),
                }
            )
        )
        res = yield unknown_box.read_message()
        assert res is None

    @gen_test(timeout=2)
    def test_websocket_pass_to_nanomsg(self):
        """WebSocketで受け取ったModuleからのMessageに適切なtimestamp/countを付与してnanomsgに流せているかどうか."""

        # make dummy environ
        with MetaDataSession.begin():
            user = User.create(account='tester', password='tester')
            user.renew_token()
            schema = Schema.create(display_name='Schema', properties='x:int,y:float')
            module = Module.create(display_name='Module')
            mbox = MessageBox(
                uuid='4ffab839-cf56-478a-8614-6003a5980855', schema_uuid=schema.uuid, module_uuid=module.uuid
            )

            MetaDataSession.add(user)
            MetaDataSession.add(schema)
            MetaDataSession.add(module)
            MetaDataSession.add(mbox)

        dummy_module = yield websocket_connect(
            httpclient.HTTPRequest(
                self.get_url('/modules/{}/{}'.format(module.uuid, mbox.uuid)),
                headers={
                    'Authorization': 'Bearer {token}'.format(token=user.encoded_token),
                }
            )
        )
        dummy_module.write_message(json.dumps({'x': 1, 'y': 2}))

        # 素直にrecvするとIOLoopがブロックされてModuleHandlerが何も返せなくなるのでModuleHandlerをまず動かす
        yield sleep(1)
        self.datareceiver.receive_new_message.assert_called_once_with(
            '4ffab839-cf56-478a-8614-6003a5980855', {
                'x': 1,
                'y': 2
            }
        )
