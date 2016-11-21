from circle_core.helpers.topics import WriteDB, TOPIC_LENGTH
from circle_core.helpers import logger
from circle_core.helpers.nanomsg import Receiver


def run():
    topic = WriteDB
    receiver = Receiver()
    for msg in receiver.incoming_messages(topic):
        logger.debug('received a message "%s" in topic %s', msg, topic)
