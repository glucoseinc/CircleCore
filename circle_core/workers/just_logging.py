# -*- coding: utf-8 -*-

"""JustLoggingに流れているメッセージを標準出力に出す."""

# system module
from logging import getLogger

# project module
from ..helpers.nanomsg import Receiver
from ..helpers.topics import JustLogging

logger = getLogger(__name__)


def run():
    """clickから起動される."""
    topic = JustLogging
    receiver = Receiver()
    for msg in receiver.incoming_messages(topic):
        logger.debug('received a message %r in topic %s', msg, topic)
