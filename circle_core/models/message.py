# -*- coding: utf-8 -*-
"""デバイスからのメッセージ."""
import decimal
import json
import re
from time import time
from uuid import UUID

from base58 import b58decode
from click import get_current_context

from .module import Module
from .schema import Schema
from ..exceptions import SchemaNotFoundError
from ..helpers.metadata import metadata
from ..logger import get_stream_logger


logger = get_stream_logger(__name__)
message_timestamp_context = decimal.Context(16, decimal.ROUND_DOWN)


class ModuleMessageFactory(object):
    """新しいModuleMessageのためのtimestamp/countを管理する責務を持つ

    :param Dict[str, ModuleMessage] last_message_per_module:
    """

    last_message_per_module = {}

    @classmethod
    def new(cls, module_uuid, json_msg):
        """
        :param UUID module_uuid:
        :param str plain_msg:
        :return ModuleMessage:
        """
        timestamp = round(time(), 6)  # TODO: Python内ではdatetimeで統一
        last_message = cls.last_message_per_module.get(module_uuid, None)
        if last_message is not None and 32767 > last_message.count:
            count = last_message.count + 1
        else:
            count = 0

        cls.last_message_per_module[module_uuid] = ModuleMessage(module_uuid, json_msg, timestamp, count)
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
    def decode(cls, plain_msg):
        """encodeの対.

        :param str plain_msg:
        :return ModuleMessage:
        """
        decoded = json.loads(plain_msg)
        return cls(**decoded)

    @classmethod
    def make_timestamp(cls, timestamp):
        assert isinstance(timestamp, (float, decimal.Decimal))

        if isinstance(timestamp, float):
            return message_timestamp_context.create_decimal_from_float(timestamp)
        else:
            return message_timestamp_context.create_decimal(timestamp)

    @classmethod
    def is_equal_timestamp(cls, x, y):
        return message_timestamp_context.compare(
            cls.make_timestamp(x),
            cls.make_timestamp(y)
        ).is_zero()

    def __init__(self, module_uuid, payload, timestamp, count):
        """timestampとcountをMessageの識別子とする.

        :param UUID module_uuid:
        :param dict payload:
        :param float_or_Deciaml timestamp:
        :param int count:
        """
        self.payload = payload
        self.timestamp = self.make_timestamp(timestamp)
        self.count = count

        if not isinstance(module_uuid, UUID):
            module_uuid = UUID(module_uuid)

        self.module = metadata().find_module(module_uuid)
        boxes = [metadata().find_message_box(box_uuid) for box_uuid in self.module.message_box_uuids]
        schemas = [metadata().find_schema(box.schema_uuid) for box in boxes]
        try:
            self.schema = [schema for schema in schemas if schema.is_valid(payload)][0]
        except IndexError:
            logger.error(
                'Known schemas: %r',
                [{property.name: property.type for property in schema.properties} for schema in metadata().schemas]
            )
            logger.error(
                'Schema of the received message: %r',
                {key: type(value) for key, value in payload.items()}
            )
            raise SchemaNotFoundError()

    def encode(self):
        """slaveのCircleCoreに送られる際に使われる.

        :return str:
        """
        return json.dumps({
            'timestamp': float(self.timestamp),
            'count': self.count,
            'module_uuid': self.module.uuid.hex,
            'payload': self.payload
        })
