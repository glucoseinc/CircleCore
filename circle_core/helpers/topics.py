# -*- coding: utf-8 -*-
"""nanomsgでPubSubする際のTopic(部屋名)を表すクラス群."""
import uuid

from base58 import b58decode, b58encode


TOPIC_LENGTH = 64  # Topic name must be shorter than this value
# UUIDをbase58encodeしたものの長さは22chars


def make_topic(topic):
    assert isinstance(topic, str)
    assert len(topic) < TOPIC_LENGTH
    return topic.ljust(TOPIC_LENGTH)


def make_message_topic(module_id=None, box_id=None):
    """新しいMessageが投げられた時のtopic"""
    assert module_id is None or isinstance(module_id, uuid.UUID)
    assert box_id is None or isinstance(box_id, uuid.UUID)

    t = ['message']
    if module_id:
        t.append(b58encode(module_id.bytes))
        if box_id:
            t.append(b58encode(box_id.bytes))
    return make_topic(':'.join(t))
