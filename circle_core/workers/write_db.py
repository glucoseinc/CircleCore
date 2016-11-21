#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""DBを弄るワーカー?."""
from circle_core.helpers.topics import WriteDB, TOPIC_LENGTH
from circle_core.helpers import logger
from circle_core.helpers.nanomsg import Receiver


def run():
    """とりあえずWriteDBに流れてるメッセージをロギングする.

    clickから起動される
    """
    topic = WriteDB
    receiver = Receiver()
    for msg in receiver.incoming_messages(topic):
        logger.debug('received a message "%s" in topic %s', msg, topic)
