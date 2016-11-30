# -*- coding: utf-8 -*-
from os.path import join
from tempfile import mkdtemp

from nnpy import AF_SP, PUB, Socket, SUB, SUB_SUBSCRIBE
import pytest

from circle_core.helpers.nanomsg import get_ipc_socket_path, Receiver, Sender  # TODO: flake8-import-orderの設定
from circle_core.helpers.topics import TopicBase


class TestTopic(TopicBase):
    pass


class TestReceiver(object):
    @classmethod
    def setup_class(cls):
        cls.socket = Socket(AF_SP, PUB)
        cls.socket.bind(get_ipc_socket_path())
        cls.receiver = Receiver()
        cls.messages = cls.receiver.incoming_messages(TestTopic)

    @classmethod
    def teardown_class(cls):
        cls.socket.close()
        del cls.receiver

    @pytest.mark.timeout(1)
    def test_json(self):
        self.socket.send(TestTopic.encode_json({u'body': u"I'm in body"}))
        assert next(self.messages) == {u'body': u"I'm in body"}

    @pytest.mark.timeout(1)
    def test_multibyte_json(self):
        self.socket.send(TestTopic.encode_json({u'鍵': u'値'}).encode('utf-8'))
        assert next(self.messages) == {u'鍵': u'値'}

    @pytest.mark.timeout(1)
    def test_blocking(self):  # Receiver側で受け取ったメッセージの処理が終わらない内に次のメッセージが来た場合
        self.socket.send(TestTopic.encode_json({u'count': 1}))
        self.socket.send(TestTopic.encode_json({u'count': 2}))
        assert next(self.messages) == {u'count': 1}
        assert next(self.messages) == {u'count': 2}

    @pytest.mark.timeout(1)
    def test_close(self):
        return  # TODO
        self.socket.send(TestTopic.encode_text(u'this message is sent to limbo').encode('utf-8'))
        del self.receiver
        assert next(self.messages, None) is None


class TestSender(object):
    @classmethod
    def setup_class(cls):
        cls.sender = Sender()
        cls.socket = Socket(AF_SP, SUB)
        cls.socket.connect(get_ipc_socket_path())
        cls.socket.setsockopt(SUB, SUB_SUBSCRIBE, '')

    @classmethod
    def teardown_class(cls):
        del cls.sender
        cls.socket.close()

    @pytest.mark.timeout(1)
    def test_text(self):
        self.sender.send(u'this message is belonging to no topic')
        assert self.socket.recv().decode('utf-8') == 'this message is belonging to no topic'

    @pytest.mark.timeout(1)
    def test_multibyte_text(self):
        self.sender.send(u'こんにちは')
        assert self.socket.recv().decode('utf-8') == u'こんにちは'
