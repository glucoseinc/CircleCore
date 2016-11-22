#!/usr/bin/env python
# -*- coding: utf-8 -*-
from circle_core.helpers.nanomsg import Receiver
from circle_core.helpers.topics import WriteDB
import pytest
from websocket import create_connection


class TestSensorHandler:
    @classmethod
    def setup_class(cls):
        # FIXME: Tornadoサーバーをバックグラウンドで立てる方法がわからなかった。裏で`crcr server run`済みとする。
        cls.receiver = Receiver()
        cls.messages = cls.receiver.incoming_messages(WriteDB)
        cls.ws = create_connection('ws://127.0.0.1:5000/ws')

    @classmethod
    def teardown_class(cls):
        cls.ws.close()
        del cls.receiver

    @pytest.mark.timeout(1)
    def test_simple(self):
        self.ws.send('hoge')
        assert next(self.messages) == 'hoge'  # 本来は各ワーカーへの指示が飛ぶことになると思うが今はとりあえず
