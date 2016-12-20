# -*- coding: utf-8 -*-
import json

from nnpy import AF_SP, PUB, Socket, SUB, SUB_SUBSCRIBE
import pytest

from circle_core.helpers.nanomsg import get_ipc_socket_path, Receiver, Sender  # TODO: flake8-import-orderの設定
from circle_core.helpers.topics import BaseTopic, TOPIC_LENGTH
from circle_core.models.message import Message
from circle_core.models.module import Module
from circle_core.models.schema import Schema


class DummyTopic(BaseTopic):
    pass


class DummyMessage(Message):
    @property
    def _metadata(self):
        return DummyMetadata

    def decode(self, msg):
        self.module = self._metadata.modules[0]
        self.payload = json.loads(msg[TOPIC_LENGTH:])


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

    @classmethod
    def find_schema(cls, *args):
        return cls.schemas[0]


class TestReceiver(object):
    @classmethod
    def setup_class(cls):
        cls.socket = Socket(AF_SP, PUB)
        cls.socket.bind(get_ipc_socket_path())
        cls.receiver = Receiver(DummyTopic(), DummyMessage)
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
