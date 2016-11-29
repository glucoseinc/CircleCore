#!/usr/bin/env python
# -*- coding: utf-8 -*-
from circle_core.helpers.nanomsg import Receiver
from circle_core.helpers.topics import JustLogging
import pytest
import tcptest
from websocket import create_connection


class CircleCoreTestServer(tcptest.TestServer):
    def build_command(self):
        return 'crcr', 'server', 'run', '--port', str(self.port)


class TestSensorHandler(object):
    @classmethod
    def setup_class(cls):
        cls.server = CircleCoreTestServer()
        cls.server.start()
        cls.receiver = Receiver()
        cls.messages = cls.receiver.incoming_messages(JustLogging)
        cls.ws = create_connection('ws://127.0.0.1:{}/ws'.format(cls.server.port))

    @classmethod
    def teardown_class(cls):
        cls.ws.close()
        del cls.receiver
        cls.server.stop()

    @pytest.mark.timeout(1)
    def test_simple(self):
        self.ws.send(u'{"hoge": "piyo"}')
        assert next(self.messages) == {u'hoge': u'piyo'}
        # 本来は各ワーカーへの指示が飛ぶことになると思うが今はとりあえず
