# -*- coding: utf-8 -*-
"""デバイスからのメッセージ."""
import decimal
import json
import logging
import re
from time import time
from uuid import UUID

from base58 import b58decode
from click import get_current_context

from circle_core.utils import prepare_uuid
from .module import Module
from .schema import Schema
from ..exceptions import MessageBoxNotFoundError, SchemaNotFoundError, SchemaNotMatchError
# from ..helpers.metadata import metadata
# from ..logger import get_stream_logger


logger = logging.getLogger(__name__)
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
        payload = json_msg.copy()

        # primary key(timestmap, count)を決定する
        timestamp = time()
        # TODO: このあたり厳密にはCASをしないとならないはず
        last_message = cls.last_message_per_module.get(module_uuid, None)
        if last_message is not None and 32767 > last_message.count:
            count = last_message.count + 1
        else:
            count = 0

        # message boxを決定
        box_id = UUID(payload.pop('_box'))

        # boxがあるか確認
        box = metadata().find_message_box(box_id)
        if not box:
            raise MessageBoxNotFoundError()

        schema = metadata().find_schema(box.schema_uuid)
        if not schema:
            raise SchemaNotFoundError()

        if not schema.is_valid(payload):
            logger.error(
                'Schema of the received message: %r',
                {key: type(value) for key, value in payload.items()}
            )
            raise SchemaNotMatchError()

        #
        new_message = ModuleMessage(module_uuid, box_id, timestamp, count, payload)

        cls.last_message_per_module[module_uuid] = new_message
        return new_message


class ModuleMessage(object):
    """CircleModuleからのメッセージ.

    :param UUID module_uuid:
    :param MessageBox message_box:
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
        json_msg = json.loads(plain_msg)
        timestamp = message_timestamp_context.create_decimal(json_msg.pop('timestamp'))
        return cls(timestamp=timestamp, **json_msg)

    @classmethod
    def make_timestamp(cls, timestamp):
        assert isinstance(timestamp, (float, str, decimal.Decimal))

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

    def __repr__(self):
        return '<circle_core.models.message.ModuleMessage %s>' % self.encode()

    def __init__(self, module_uuid, box_id, timestamp, count, payload):
        """timestampとcountをMessageの識別子とする.

        :param UUID module_uuid:
        :param UUID box_id:
        :param dict payload:
        :param Union[str, Decimal] timestamp:
        :param int count:
        :param dict payload:
        """
        self.module_uuid = prepare_uuid(module_uuid)
        self.box_id = prepare_uuid(box_id)
        self.timestamp = self.make_timestamp(timestamp)
        self.count = count
        self.payload = payload

    def encode(self):
        """slaveのCircleCoreに送られる際に使われる.

        :return str:
        """
        return json.dumps({
            'timestamp': str(self.timestamp),
            'count': self.count,
            'module_uuid': self.module_uuid.hex,
            'box_id': self.box_id.hex,
            'payload': self.payload
        })
