#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""nanomsgでPubSubする際のTopic(部屋名)を表すクラス群."""
import json
import re


TOPIC_LENGTH = 25  # Topic name must be shorter than this value


class TopicBase(object):
    """全てのTopicの基底クラス."""

    @classmethod
    def justify(cls):
        """Topic名の長さをTOPIC_LENGTHに揃えて返す.

        :return str:
        """
        return cls.__name__.ljust(TOPIC_LENGTH)

    @classmethod
    def with_json(cls, data):
        """Topic名と引数を繋げて返す.

        特定のTopicに向けてメッセージを送る際に有用

        :param unicode data: 送りたいJSON
        :return unicode:
        """
        return cls.justify() + data

    @classmethod
    def encode_json(cls, data):
        """Topic名と引数を繋げて返す.

        特定のTopicに向けてメッセージを送る際に有用

        :param dict data: JSONにして送りたいデータ
        :return unicode:
        """
        return cls.justify() + json.dumps(data, ensure_ascii=False)

    @classmethod
    def decode_json(cls, data):
        """nanomsgで送られてきたJSONからトピック名を取り除いて返す.

        :param unicode data:
        :return dict:
        """
        return json.loads(re.sub('^' + cls.justify(), '', data))


class WriteDB(TopicBase):
    """DBを扱うワーカーがsubscribeするTopic?."""

    pass
