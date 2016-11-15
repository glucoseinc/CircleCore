from circle_core.topics import WriteDB, TOPIC_LENGTH
from circle_core.utils import logger
from circle_core.workers.utils import NanomsgReceiver


def run():
    topic = WriteDB
    receiver = NanomsgReceiver()
    for msg in receiver.incoming_messages(topic):
        logger.debug('received a message "%s" in topic %s', msg[TOPIC_LENGTH:], topic)
