# -*- coding: utf-8 -*-
from multiprocessing import Process
from time import sleep

import pytest
from websocket import create_connection

from circle_core.helpers.nanomsg import Receiver
from circle_core.helpers.topics import JustLogging
from circle_core.server import ws


class TestSensorHandler(object):
    @classmethod
    def setup_class(cls):
        cls.receiver = Receiver()
        cls.messages = cls.receiver.incoming_messages(JustLogging)
        cls.server = Process(target=ws.run, args=['/', 5000])
        cls.server.daemon = True
        cls.server.start()
        sleep(0.1)
        cls.ws = create_connection('ws://localhost:5000/')

    @classmethod
    def teardown_class(cls):
        del cls.receiver
        cls.ws.close()
        cls.server.terminate()

    @pytest.mark.timeout(1)
    def test_simple(self):
        self.ws.send(u'{"hoge": "piyo"}')
        assert next(self.messages) == {u'hoge': u'piyo'}
        # 本来は各ワーカーへの指示が飛ぶことになると思うが今はとりあえず
