# -*- coding: utf-8 -*-
import json

from nnpy import AF_SP, PUB, Socket, SUB, SUB_SUBSCRIBE
import pytest

from circle_core.helpers.nanomsg import get_ipc_socket_path, Receiver, Sender  # TODO: flake8-import-orderの設定
from circle_core.helpers.topics import BaseTopic, TOPIC_LENGTH
from circle_core.models import message
from circle_core.models.message import ModuleMessage
from circle_core.models.message_box import MessageBox
from circle_core.models.metadata.base import MetadataReader
from circle_core.models.module import Module
from circle_core.models.schema import Schema


class DummyTopic(BaseTopic):
    def decode(self, plain_msg):
        payload = json.loads(plain_msg[TOPIC_LENGTH:])
        return [ModuleMessage('8e654793-5c46-4721-911e-b9d19f0779f9', payload)]


class DummyMetadata(MetadataReader):
    schemas = [
        Schema('44ae2fd8-52d0-484d-9a48-128b07937a0a', 'json', 'body:str'),
        Schema('a1912d13-8fc7-4714-8cb3-e6f9326fdb36', 'multibyte_json', '鍵:str'),
        Schema('1a7c8c61-7709-442e-9059-e8498501fb36', 'blocking', 'count:int')
    ]
    message_boxes = [
        MessageBox('316720eb-84fe-43b3-88b7-9aad49a93220', '44ae2fd8-52d0-484d-9a48-128b07937a0a'),
        MessageBox('e2ca248d-5300-4641-830f-97a4dae0d245', 'a1912d13-8fc7-4714-8cb3-e6f9326fdb36'),
        MessageBox('50ba26f6-2447-4f6a-93b1-d62051d83026', '1a7c8c61-7709-442e-9059-e8498501fb36')
    ]
    modules = [Module(
        '8e654793-5c46-4721-911e-b9d19f0779f9',
        '316720eb-84fe-43b3-88b7-9aad49a93220,e2ca248d-5300-4641-830f-97a4dae0d245,50ba26f6-2447-4f6a-93b1-d62051d83026',  # NOQA
        'DummyModule',
        'foo,bar'
    )]
    users = []
    parse_url_scheme = None


class TestReceiver(object):
    @classmethod
    def setup_class(cls):
        message.metadata = DummyMetadata
        cls.socket = Socket(AF_SP, PUB)
        cls.socket.bind(get_ipc_socket_path())
        cls.receiver = Receiver(DummyTopic())
        cls.messages = cls.receiver.incoming_messages()

    @classmethod
    def teardown_class(cls):
        cls.socket.close()
        del cls.receiver

    @pytest.mark.timeout(3)
    def test_json(self):
        self.socket.send(DummyTopic().encode(u'{"body": "I\'m in body"}'))
        assert next(self.messages).payload == {u'body': u"I'm in body"}

    @pytest.mark.timeout(3)
    def test_multibyte_json(self):
        self.socket.send(DummyTopic().encode(u'{"鍵": "値"}').encode('utf-8'))
        assert next(self.messages).payload == {u'鍵': u'値'}

    @pytest.mark.timeout(3)
    def test_blocking(self):  # Receiver側で受け取ったメッセージの処理が終わらない内に次のメッセージが来た場合
        self.socket.send(DummyTopic().encode(u'{"count": 1}'))
        self.socket.send(DummyTopic().encode(u'{"count": 2}'))
        assert next(self.messages).payload == {u'count': 1}
        assert next(self.messages).payload == {u'count': 2}

    @pytest.mark.timeout(3)
    @pytest.mark.skip  # TODO
    def test_close(self):
        self.socket.send(DummyTopic().encode(u'this message is sent to limbo').encode('utf-8'))
        del self.receiver
        assert next(self.messages, None) is None


class TestSender(object):
    @classmethod
    def setup_class(cls):
        cls.sender = Sender(DummyTopic())
        cls.socket = Socket(AF_SP, SUB)
        cls.socket.connect(get_ipc_socket_path())
        cls.socket.setsockopt(SUB, SUB_SUBSCRIBE, '')

    @classmethod
    def teardown_class(cls):
        del cls.sender
        cls.socket.close()

    @pytest.mark.timeout(3)
    def test_text(self):
        self.sender.send('this message is belonging to DummyTopic')
        assert self.socket.recv().decode('utf-8')[TOPIC_LENGTH:] == 'this message is belonging to DummyTopic'

    @pytest.mark.timeout(3)
    def test_multibyte_text(self):
        self.sender.send(u'このメッセージはDummyTopicに紐付いています')
        assert self.socket.recv().decode('utf-8')[TOPIC_LENGTH:] == u'このメッセージはDummyTopicに紐付いています'
