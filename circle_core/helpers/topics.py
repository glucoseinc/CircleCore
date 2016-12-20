# -*- coding: utf-8 -*-
"""nanomsgでPubSubする際のTopic(部屋名)を表すクラス群."""
import json
import re
from uuid import UUID

from base58 import b58encode
from werkzeug import cached_property


TOPIC_LENGTH = 48  # Topic name must be shorter than this value


class BaseTopic(object):
    """nanomsgのTopicを表す.

    受け取ったデータをnanomsgで送れるテキストに変換する責務を持つ。
    受信後の復元、その後の取り回しはMessageの役割。
    """

    @cached_property
    def topic(self):
        """Topic名."""
        return self.__class__.__name__

    def encode(self, text):
        """Topicとtextを繋げて返す.

        :param unicode text: 送りたいプレーンテキスト
        :return unicode:
        """
        return self.topic.ljust(TOPIC_LENGTH) + text


class JustLogging(BaseTopic):
    """特に意味のないTopic."""

    @cached_property
    def topic(self):
        return ''


class SensorDataTopic(BaseTopic):
    """センサデータの送受信Topic."""

    prefix = 'module:'

    def __init__(self, module=None):
        """constructor."""
        self.module = module

    @cached_property
    def topic(self):
        if self.module:
            return self.prefix + b58encode(self.module.uuid.bytes)
        else:
            return self.prefix
