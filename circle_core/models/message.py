# -*- coding: utf-8 -*-
"""デバイスからのメッセージ."""
import json
import re
from time import time
from uuid import UUID

from base58 import b58decode
from click import get_current_context

from ..logger import get_stream_logger


logger = get_stream_logger(__name__)


def metadata():
    """テスト時に上書き.

    もっといい方法ないかな
    """
    return get_current_context().obj.metadata


class ModuleMessage(object):
    """CircleModuleからのメッセージ.

    :param Dict[str, Message] last_message_per_module:
    :param Module module_uuid:
    :param Schema schema:
    :param int timestamp:
    :param int count:
    :param dict payload:
    """

    last_message_per_module = {}

    @classmethod
    def decode(cls, json_msg):
        """encodeの対.

        :return ModuleMessage:
        """
        return cls(**json_msg)

    def __init__(self, module_uuid, payload, timestamp=None, count=None):
        """timestampとcountをMessageの識別子とする.

        :param UUID module_uuid:
        :param dict payload:
        """
        self.payload = payload

        if not isinstance(module_uuid, UUID):
            module_uuid = UUID(module_uuid)

        self.module = metadata().find_module(module_uuid)
        boxes = [metadata().find_message_box(box_uuid) for box_uuid in self.module.message_box_uuids]
        schemas = [metadata().find_schema(box.schema_uuid) for box in boxes]
        try:
            self.schema = [schema for schema in schemas if schema.is_valid(payload)][0]
        except IndexError:
            logger.error('Known schemas: %r', [(hoge.name, hoge.type) for hoge in metadata().schemas[0].properties])
            logger.error(
                'Schema of the received message: %r',
                {key: type(value) for key, value in payload.items()}
            )
            raise ValueError('Schema of a received message is unknown')

        if timestamp and count:
            self.timestamp = timestamp
            self.count = count
            return

        self.timestamp = round(time(), 6)  # datetimeはJSON Serializableではないので
        if self.last_message is not None and self.last_message.timestamp == self.timestamp:
            self.count = self.last_message.count + 1
        else:
            self.count = 0
            self.last_message = self

    @property
    def last_message(self):
        """このメッセージを送ったモジュールからの一つ前のメッセージ."""
        return self.last_message_per_module.get(self.module.uuid.hex, None)

    @last_message.setter
    def last_message(self, msg):
        self.last_message_per_module[self.module.uuid.hex] = msg

    def encode(self):
        """slaveのCircleCoreに送られる際に使われる.

        :return str:
        """
        return json.dumps({
            'timestamp': self.timestamp,
            'count': self.count,
            'module': self.module.uuid.hex,
            'payload': self.payload
        })
