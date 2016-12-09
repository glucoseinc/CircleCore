# -*- coding: utf-8 -*-
"""nanomsgでPubSubする際のTopic(部屋名)を表すクラス群."""
import json
import re
from uuid import UUID

import base58
from werkzeug import cached_property


TOPIC_LENGTH = 48  # Topic name must be shorter than this value


class TopicBase(object):
    """全てのTopicの基底クラス."""

    @property
    def topic(self):
        return self.__class__.__name__.ljust(TOPIC_LENGTH)

    def with_json(self, jsondata):
        """Topic名と引数を繋げて返す.

        特定のTopicに向けてメッセージを送る際に有用

        :param unicode data: 送りたいJSON
        :return unicode:
        """
        return self.topic + jsondata

    def encode_json(self, data):
        """Topic名と引数を繋げて返す.

        特定のTopicに向けてメッセージを送る際に有用

        :param dict data: JSONにして送りたいデータ
        :return unicode:
        """
        return self.topic + json.dumps(data, ensure_ascii=False)

    def decode_json(self, data):
        """nanomsgで送られてきたJSONからトピック名を取り除いて返す.

        :param unicode data:
        :return dict:
        """
        return json.loads(re.sub('^' + self.topic, '', data))


class JustLogging(TopicBase):
    """特に意味のないTopic."""

    @property
    def topic(self):
        return ''


class SensorDataTopic(TopicBase):
    """センサデータの送受信Topic
    送受信わけるべきでは?"""

    topic_prefix = 'module:'

    def __init__(self, module=None):
        self.module = module

    @classmethod
    def topic_for_module(cls, module):
        return '{}{}'.format(
            cls.topic_prefix,
            base58.b58encode(module.uuid.bytes)
        ).ljust(TOPIC_LENGTH)

    @cached_property
    def topic(self):
        if self.module:
            return self.topic_for_module(self.module)
        else:
            return self.topic_prefix

    def decode_json(self, data):
        """nanomsgで送られてきたJSONからトピック名を取り除いて返す.

        :param unicode data:
        :return dict:
        """
        topic, jsondata = data[:TOPIC_LENGTH], data[TOPIC_LENGTH:]
        module_uuid = UUID(bytes=base58.b58decode(topic[len(self.topic_prefix):].rstrip()))

        return module_uuid, json.loads(jsondata)
