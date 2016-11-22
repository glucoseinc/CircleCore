#!/usr/bin/env python
# -*- coding: utf-8 -*-
from os.path import join
from tempfile import mkdtemp

from circle_core.helpers.nanomsg import Receiver, Sender  # TODO: flake8-import-orderの設定
from circle_core.helpers.topics import TopicBase
from nnpy import AF_SP, PUB, Socket, SUB, SUB_SUBSCRIBE
import pytest


SOCKET_PATH = 'ipc://' + join(mkdtemp(), 'socket.ipc')


class TestTopic(TopicBase):
    pass


class TestReceiver:
    @classmethod
    def setup_class(cls):
        cls.socket = Socket(AF_SP, PUB)
        cls.socket.bind(SOCKET_PATH)
        cls.receiver = Receiver(SOCKET_PATH)
        cls.messages = cls.receiver.incoming_messages(TestTopic)

    @classmethod
    def teardown_class(cls):
        cls.socket.close()
        del cls.receiver

    @pytest.mark.timeout(1)
    def test_simple(self):
        self.socket.send(TestTopic.text('this is test message'))
        assert next(self.messages) == 'this is test message'

    @pytest.mark.timeout(1)
    def test_blocking(self):  # Receiver側で受け取ったメッセージの処理が終わらない内に次のメッセージが来た場合
        self.socket.send(TestTopic.text('message one'))
        self.socket.send(TestTopic.text('message two'))
        assert next(self.messages) == 'message one'
        assert next(self.messages) == 'message two'

    @pytest.mark.timeout(1)
    def test_close(self):
        return  # TODO
        self.socket.send(TestTopic.text('this message is sent to limbo'))
        del self.receiver
        assert next(self.messages, None) is None


class TestSender():
    @classmethod
    def setup_class(cls):
        cls.sender = Sender(SOCKET_PATH)
        cls.socket = Socket(AF_SP, SUB)
        cls.socket.connect(SOCKET_PATH)
        cls.socket.setsockopt(SUB, SUB_SUBSCRIBE, '')

    @classmethod
    def teardown_class(cls):
        del cls.sender
        cls.socket.close()

    @pytest.mark.timeout(1)
    def test_simple(self):
        self.sender.send('this message is belonging to no topic')
        assert self.socket.recv().decode('utf-8') == 'this message is belonging to no topic'
