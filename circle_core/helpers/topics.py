# -*- coding: utf-8 -*-
"""nanomsgでPubSubする際のTopic(部屋名)を表すクラス群."""
# import json
# import re
import uuid

from base58 import b58decode, b58encode
# from werkzeug import cached_property

# from circle_core.models.message import ModuleMessage


TOPIC_LENGTH = 64  # Topic name must be shorter than this value

# UUIDをbase58encodeしたものの長さは22chars


def make_topic(topic):
    assert isinstance(topic, str)
    assert len(topic) < TOPIC_LENGTH
    return topic.ljust(TOPIC_LENGTH)


def make_message_topic(module_id, box_id):
    """新しいMessageが投げられた時のtopic"""
    assert isinstance(module_id, uuid.UUID)
    assert isinstance(box_id, uuid.UUID)

    return make_topic('message:{}:{}'.format(
        b58encode(module_id.bytes),
        b58encode(box_id.bytes)
    ))
