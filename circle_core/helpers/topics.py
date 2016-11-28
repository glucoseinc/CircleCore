#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""nanomsgでPubSubする際のTopic(部屋名)を表すクラス群."""
import json
import re


TOPIC_LENGTH = 25  # Topic name must be shorter than this value


class TopicBase:
    """全てのTopicの基底クラス."""

    @classmethod
    def justify(cls):
        """Topic名の長さをTOPIC_LENGTHに揃えて返す.

        :return str:
        """
        return cls.__name__.ljust(TOPIC_LENGTH)

    @classmethod
    def encode_text(cls, msg):
        """Topic名と引数を繋げて返す.

        特定のTopicに向けてメッセージを送る際に有用

        :param unicode msg: 送りたいメッセージ
        :return unicode:
        """
        return cls.justify() + msg

    @classmethod
    def decode_text(cls, msg):
        """nanomsgで送られてきたメッセージからトピック名を取り除いて返す.

        :param unicode msg:
        :return unicode:
        """
        return re.sub('^' + cls.justify(), '', msg)


class WriteDB(TopicBase):
    """DBを扱うワーカーがsubscribeするTopic?."""

    pass
