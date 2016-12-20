# -*- coding: utf-8 -*-
"""デバイスからのメッセージ."""
import json
import re
from time import time
from uuid import UUID

from base58 import b58decode
from click import get_current_context

from ..helpers.topics import SensorDataTopic, TOPIC_LENGTH


def metadata():
    """テスト時に上書き.

    もっといい方法ないかな
    """
    return get_current_context().obj.metadata


class Message(object):
    """デバイスからのメッセージ.

    :param Message last_message:
    :param BaseTopic topic:
    :param Module module:
    :param Schema schema:
    :param int timestamp:
    :param int count:
    :param dict payload:
    """

    topic = SensorDataTopic
    last_message = None  # 別のプロセスで動いているものは別のテーブルに書き込もうとするので重複は気にしなくていい

    def __init__(self, msg):
        """timestampとcountをMessageの識別子とする.

        :param Module module:
        :param str msg:
        """
        self.decode(msg)
        self.schema = metadata().find_module(self.module.uuid)

        self.timestamp = time()
        if self.last_message is not None and self.last_message.timestamp == self.timestamp:
            self.count = self.last_message.count + 1
        else:
            self.count = 0

        self.last_message = self

    def decode(self, msg):
        """nanomsgで送られてきたメッセージがJSONだとしてデシリアライズ.

        :param str msg:
        """
        module_uuid = UUID(bytes=b58decode(msg[len(self.topic.prefix):TOPIC_LENGTH].rstrip()))
        self.module = metadata().find_module(module_uuid)
        self.payload = json.loads(msg[TOPIC_LENGTH:])

    def encode(self):
        """slaveのCircleCoreに送られる際に使われる.

        :return str:
        """
        return json.dumps({
            'timestamp': self.timestamp,
            'count': self.count,
            'module': self.module.uuid.hex,
            'payload': self.payload
        })
