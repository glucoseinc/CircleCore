# -*- coding: utf-8 -*-
"""nanomsgでPubSubする際のTopic(部屋名)を表すクラス群."""

# system module
import uuid
from typing import Optional

# community module
from base58 import b58encode

TOPIC_LENGTH = 64  # Topic name must be shorter than this value

# UUIDをbase58encodeしたものの長さは22chars


def make_topic(topic: str) -> str:
    """topicを作成する.

    Args:
        topic: Topic

    Return:
        topic
    """
    assert isinstance(topic, str)
    assert len(topic) < TOPIC_LENGTH
    return topic.ljust(TOPIC_LENGTH)


def make_message_topic(module_id: Optional[uuid.UUID] = None, box_id: Optional[uuid.UUID] = None) -> str:
    """新しいMessageが投げられた時のtopicを作成する.

    Args:
        module_id: Module UUID
        box_id: MessageBox UUID

    Return:
        topic
    """
    assert module_id is None or isinstance(module_id, uuid.UUID)
    assert box_id is None or isinstance(box_id, uuid.UUID)

    t = ['message']
    if module_id:
        t.append(b58encode(module_id.bytes).decode('latin1'))
        if box_id:
            t.append(b58encode(box_id.bytes).decode('latin1'))
    return make_topic(':'.join(t))
