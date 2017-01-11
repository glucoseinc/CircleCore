# -*- coding: utf-8 -*-
"""JustLoggingに流れているメッセージを標準出力に出す."""

# project module
from circle_core.logger import get_stream_logger
from ..helpers.nanomsg import Receiver
from ..helpers.topics import JustLogging

logger = get_stream_logger(__name__)


def run(config):
    """clickから起動される."""
    topic = JustLogging()
    receiver = Receiver(topic)
    for msg in receiver.incoming_messages():
        logger.debug('received a message %r in topic %s', msg, topic)
