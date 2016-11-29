#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""JustLoggingに流れているメッセージを標準出力に出す."""
from circle_core.helpers import logger
from circle_core.helpers.nanomsg import Receiver
from circle_core.helpers.topics import JustLogging


def run():
    """clickから起動される."""
    topic = JustLogging
    receiver = Receiver()
    for msg in receiver.incoming_messages(topic):
        logger.debug('received a message %r in topic %s', msg, topic)
