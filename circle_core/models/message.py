# -*- coding: utf-8 -*-
"""デバイスからのメッセージ."""
import json
import re
from time import time

from ..helpers import TOPIC_LENGTH


class Message(object):
    """デバイスからのメッセージ.

    :param Message last_message:
    :param Module module:
    :param Schema schema:
    :param int timestamp:
    :param int count:
    :param payload:
    """
    last_message = None  # 別のプロセスで動いているものは別のテーブルに書き込もうとするので重複は気にしなくていい

    def __init__(self, module, msg):
        """timestampとcountをMessageの識別子とする.

        :param Module module:
        :param str msg:
        """
        self.module = module
        self.schema = None  # TODO: moduleに紐付いているSchemaを入れる
        self.payload = self.decode(msg)
        self.timestamp = time()

        if self.last_message is not None and self.last_message.timestamp == self.timestamp:
            self.count = self.last_message.count + 1
        else:
            self.count = 0

        self.last_message = self

    def decode(self, msg):
        """nanomsgで送られてきたメッセージがJSONだとしてデシリアライズ.

        :param unicode msg:
        :return dict:
        """
        return json.loads(msg[TOPIC_LENGTH:])

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
