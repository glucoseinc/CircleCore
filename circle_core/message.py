# -*- coding: utf-8 -*-
"""デバイスからのメッセージ.

このModelだけMetadata関連ではないので、ディレクトリが適切ではない...
"""
import decimal
import logging
import time
import uuid
from typing import NamedTuple, TYPE_CHECKING, Union

from .utils import prepare_uuid

if TYPE_CHECKING:
    from typing import Optional

    from .types import Payload

message_timestamp_context = decimal.Context(16, decimal.ROUND_DOWN)
logger = logging.getLogger(__name__)

Timestamp = decimal.Decimal
TimestampLike = Union[float, str, Timestamp]


class ModuleMessagePrimaryKey(NamedTuple):
    timestamp: Timestamp
    counter: int

    def to_json(self):
        assert isinstance(self.timestamp, decimal.Decimal)

        return [str(self.timestamp), self.counter]

    @classmethod
    def from_json(cls, jsonobj):
        if jsonobj is None:
            return None

        assert isinstance(jsonobj, list)

        return cls(ModuleMessage.make_timestamp(jsonobj[0]), jsonobj[1])

    @classmethod
    def origin(cls):
        return cls(ModuleMessage.make_timestamp('0'), 0)


class ModuleMessage(object):
    """CircleModuleからのメッセージ.

    :param UUID module_uuid:
    :param MessageBox message_box:
    :param Schema schema:
    :param decimal.Decimal timestamp:
    :param int counter:
    :param dict payload:
    """

    def __init__(self, box_id: uuid.UUID, timestamp: TimestampLike, counter: int, payload: 'Payload'):
        """timestampとcountをMessageの識別子とする.
        """
        assert isinstance(box_id, uuid.UUID)

        self.box_id = box_id
        self.timestamp = self.make_timestamp(timestamp)
        self.counter = counter
        self.payload = payload

    @classmethod
    def from_json(cls, data):
        return cls(prepare_uuid(data['boxId']), data['timestamp'], data['counter'], data['payload'])

    @classmethod
    def make_timestamp(cls, timestamp: 'Optional[TimestampLike]' = None) -> decimal.Decimal:
        if not timestamp:
            timestamp = time.time()
        assert isinstance(timestamp, (float, str, decimal.Decimal))

        if isinstance(timestamp, float):
            return message_timestamp_context.create_decimal_from_float(timestamp)
        else:
            return message_timestamp_context.create_decimal(timestamp)

    @classmethod
    def is_equal_timestamp(cls, x: TimestampLike, y: TimestampLike) -> bool:
        return message_timestamp_context.compare(cls.make_timestamp(x), cls.make_timestamp(y)).is_zero()

    def __repr__(self) -> str:
        return '<ModuleMessage box={} timestamp={} counter={}>'.format(
            str(self.box_id),
            str(self.timestamp),
            self.counter,
        )

    @property
    def primary_key(self) -> ModuleMessagePrimaryKey:
        return ModuleMessagePrimaryKey(self.timestamp, self.counter)

    def to_json(self, *, with_boxid: bool = True) -> dict:
        """slaveのCircleCoreに送られる際に使われる.
        # TODO: Deprecated

        :return str:
        """
        d = {
            'timestamp': str(self.timestamp),
            'counter': self.counter,
            'payload': self.payload,
        }
        if with_boxid:
            d['boxId'] = self.box_id.hex
        return d
