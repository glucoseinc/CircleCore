# -*- coding: utf-8 -*-
"""デバイスからのメッセージ."""
import json
import re
from time import time
from uuid import UUID

from base58 import b58decode
from click import get_current_context

from ..logger import get_stream_logger
from ..helpers.metadata import metadata
from .module import Module
from .schema import Schema


logger = get_stream_logger(__name__)


class ModuleMessageFactory(object):
    """新しいModuleMessageのためのtimestamp/countを管理する責務を持つ

    :param Dict[str, ModuleMessage] last_message_per_module:
    """

    last_message_per_module = {}

    @classmethod
    def new(cls, module_uuid, payload):
        """
        :param UUID module_uuid:
        :param dict payload:
        :return ModuleMessage:
        """
        timestamp = round(time(), 6)  # TODO: Python内ではdatetimeで統一
        last_message = cls.last_message_per_module.get(module_uuid, None)
        if last_message is not None and 32767 > last_message.count:
            count = last_message.count + 1
        else:
            count = 0

        cls.last_message_per_module[module_uuid] = ModuleMessage(module_uuid, payload, timestamp, count)
        return cls.last_message_per_module[module_uuid]


class ModuleMessage(object):
    """CircleModuleからのメッセージ.

    :param Module module:
    :param Schema schema:
    :param int timestamp:
    :param int count:
    :param dict payload:
    """

    @classmethod
    def decode(cls, json_msg):
        """encodeの対.

        :param str plain_msg:
        :return ModuleMessage:
        """
        decoded = json.loads(json_msg)
        return cls(**decoded)

    def __init__(self, module_uuid, payload, timestamp, count):
        """timestampとcountをMessageの識別子とする.

        :param UUID module_uuid:
        :param dict payload:
        :param int timestamp:
        :param int count:
        """
        self.payload = payload
        self.timestamp = timestamp
        self.count = count

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
            raise ValueError('Received message has unknow schema')

    def encode(self):
        """slaveのCircleCoreに送られる際に使われる.

        :return str:
        """
        return json.dumps({
            'timestamp': self.timestamp,
            'count': self.count,
            'module_uuid': self.module.uuid.hex,
            'payload': self.payload
        })
