# -*- coding: utf-8 -*-
"""デバイスからのメッセージ."""
from collections import namedtuple
import decimal
import re
import time
import uuid

from base58 import b58decode
from click import get_current_context

from circle_core.models import Module, Schema
from circle_core.utils import prepare_uuid
from .base import logger
from ..exceptions import MessageBoxNotFoundError, SchemaNotFoundError, SchemaNotMatchError


message_timestamp_context = decimal.Context(16, decimal.ROUND_DOWN)


class ModuleMessagePrimaryKey(
    namedtuple('ModuleMessagePrimaryKey', 'timestamp counter')
):
    def __new__(cls, t, c):
        assert isinstance(t, decimal.Decimal)
        assert isinstance(c, int)

        return super(ModuleMessagePrimaryKey, cls).__new__(cls, t, c)

    def to_json(self):
        assert isinstance(self.timestamp, decimal.Decimal)

        return [str(self.timestamp), self.counter]

    @classmethod
    def from_json(cls, jsonobj):
        if jsonobj is None:
            return None

        assert isinstance(jsonobj, list)

        return cls(
            ModuleMessage.make_timestamp(jsonobj[0]),
            jsonobj[1]
        )


class ModuleMessage(object):
    """CircleModuleからのメッセージ.

    :param UUID module_uuid:
    :param MessageBox message_box:
    :param Schema schema:
    :param decimal.Decimal timestamp:
    :param int counter:
    :param dict payload:
    """

    def __init__(self, box_id, timestamp, counter, payload):
        """timestampとcountをMessageの識別子とする.

        :param uuid.UUID box_id:
        :param dict payload:
        :param Union[str, Decimal] timestamp:
        :param int count:
        :param dict payload:
        """
        assert isinstance(box_id, uuid.UUID)

        self.box_id = box_id
        self.timestamp = self.make_timestamp(timestamp)
        self.counter = counter
        self.payload = payload

    @classmethod
    def from_json(cls, data):
        return cls(
            prepare_uuid(data['boxId']),
            data['timestamp'],
            data['counter'],
            data['payload']
        )

    @classmethod
    def make_timestamp(cls, timestamp=None):
        if not timestamp:
            timestamp = time.time()
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
        return '<ModuleMessage box={} timestamp={} counter={}>'.format(
            str(self.box_id),
            str(self.timestamp),
            self.counter,
        )

    @property
    def primary_key(self):
        return ModuleMessagePrimaryKey(self.timestamp, self.counter)

    def to_json(self):
        """slaveのCircleCoreに送られる際に使われる.

        :return str:
        """
        return {
            'timestamp': str(self.timestamp),
            'counter': self.counter,
            'boxId': self.box_id.hex,
            'payload': self.payload
        }
