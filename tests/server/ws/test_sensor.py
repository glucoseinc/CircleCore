# -*- coding: utf-8 -*-
from multiprocessing import Process
from time import sleep

import pytest
from websocket import create_connection

from circle_core.helpers.nanomsg import Receiver
from circle_core.helpers.topics import JustLogging
from circle_core.server import ws


@pytest.mark.skip
class TestSensorHandler(object):
    @classmethod
    def setup_class(cls):
        class DummyModule(object):
            def __init__(self, uuid):
                self.uuid = uuid

        class DummyMetadata(object):
            def find_module(self, module_uuid, *args, **kwargs):
                from uuid import UUID
                return DummyModule(UUID(module_uuid))

        cls.receiver = Receiver(JustLogging())
        cls.receiver.set_timeout(5000)
        cls.messages = cls.receiver.incoming_messages()
        cls.server = Process(target=ws.run, args=[DummyMetadata(), '/(?P<module_uuid>[0-9A-Fa-f-]+)', 5000])
        cls.server.daemon = True
        cls.server.start()
        sleep(0.1)
        cls.ws = create_connection('ws://localhost:5000/7EE46F5E-F6B5-4098-AFB6-8608A1932F42')

    @classmethod
    def teardown_class(cls):
        del cls.receiver
        cls.ws.close()
        cls.server.terminate()

    @pytest.mark.timeout(10)
    def test_simple(self):
        self.ws.send(u'{"hoge": "piyo"}')
        assert next(self.messages) == {u'hoge': u'piyo'}
        # 本来は各ワーカーへの指示が飛ぶことになると思うが今はとりあえず
