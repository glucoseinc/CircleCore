# -*- coding: utf-8 -*-

"""nanomsgでPubSubする際のTopic(部屋名)を表すクラス群."""

# system module
import uuid

# community module
from base58 import b58encode


# type annotation
try:
    from typing import Optional
except ImportError:
    pass


TOPIC_LENGTH = 64  # Topic name must be shorter than this value
# UUIDをbase58encodeしたものの長さは22chars


def make_topic(topic):
    """topicを作成する.

    :param str topic: topic
    :return: topic
    :rtype: str
    """
    assert isinstance(topic, str)
    assert len(topic) < TOPIC_LENGTH
    return topic.ljust(TOPIC_LENGTH)


def make_message_topic(module_id=None, box_id=None):
    """新しいMessageが投げられた時のtopicを作成する.

    :param Optional[uuid.UUID] module_id: Module UUID
    :param Optional[uuid.UUID] box_id: MessageBox UUID
    :return: topic
    :rtype: str
    """
    assert module_id is None or isinstance(module_id, uuid.UUID)
    assert box_id is None or isinstance(box_id, uuid.UUID)

    t = ['message']
    if module_id:
        t.append(b58encode(module_id.bytes))
        if box_id:
            t.append(b58encode(box_id.bytes))
    return make_topic(':'.join(t))
