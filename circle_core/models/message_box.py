# -*- coding: utf-8 -*-

"""Message Box Model."""

# system module
from uuid import UUID

# community module
from six import PY3

# project module
from .base import UUIDBasedObject
from .message import ModuleMessage
from ..helpers.metadata import metadata
from ..logger import get_stream_logger
from ..utils import prepare_uuid

if PY3:
    from typing import Optional, Union


logger = get_stream_logger(__name__)


class MessageBoxError(Exception):
    pass


class MessageBox(UUIDBasedObject):
    """MessageBoxオブジェクト

    :param str key_prefix: ストレージキーのプレフィックス
    :param UUID uuid: MessageBox UUID
    :param UUID schema_uuid: Schema UUID
    :param str display_name: 表示名
    :param Optional[str] memo: メモ
    """

    key_prefix = 'message_box'

    def __init__(self, uuid, schema_uuid, display_name, memo=None, master_uuid=None):
        """init.

        :param Union[str, UUID] uuid: MessageBox UUID
        :param Union[str, UUID] schema_uuid: Schema UUID
        :param str display_name: 表示名
        :param Optional[str] memo: メモ
        :param Union[NoneType, str, UUID] master_uuid:
        """
        super(MessageBox, self).__init__(uuid)

        if not isinstance(schema_uuid, UUID):
            try:
                schema_uuid = UUID(schema_uuid)
            except ValueError:
                raise MessageBoxError('Invalid schema_uuid : {}'.format(schema_uuid))

        self.schema_uuid = schema_uuid
        self.display_name = display_name
        self.memo = memo
        if master_uuid:
            self.master_uuid = prepare_uuid(master_uuid)
        else:
            self.master_uuid = None

    def __eq__(self, other):
        """return equality.

        :param MessageBox other: other MessageBox
        :return: equality
        :rtype: bool
        """
        return all([self.uuid == other.uuid, self.schema_uuid == other.schema_uuid,
                    self.display_name == other.display_name, self.memo == other.memo])

    @property
    def module(self):
        for m in metadata().modules:
            for box_uuid in m.message_box_uuids:
                if box_uuid == self.uuid:
                    return m

    def to_json(self):
        """このモデルのJSON表現を返す.

        :return: json表現のdict
        :rtype: Dict
        """
        return {
            'uuid': str(self.uuid),
            'schema_uuid': str(self.schema_uuid),
            'display_name': self.display_name,
            'memo': self.memo,
        }

    @classmethod
    def from_json(cls, json_msg, **kwargs):
        """JSON表現からの復元.

        :param dict json_msg:
        :rtype: MessageBox
        """
        return cls(**json_msg, **kwargs)

    def messages_since(self, timestamp, count):
        """引数以降、このMessageBoxに蓄えられたModuleMessageを返す.

        :param int timestamp:
        :param int count:
        """
        from ..database import Database  # 循環importを防ぐ
        db = Database(metadata().database_url)
        table = db.find_table_for_message_box(self)
        session = db._session()
        with session.begin():
            created_at = timestamp
            query = session.query(table).filter(
                (created_at < table.columns._created_at) |
                ((table.columns._created_at == created_at) & (count < table.columns._counter))
            )
            logger.debug('Execute query %s', query)
            rows = query.all()
            logger.debug('Result: %r', rows)

            for row in rows:
                payload = {
                    key: value
                    for key, value in zip(row.keys(), row)
                    if not key.startswith('_')
                }
                timestamp = row._created_at  # timetupleを使うとmicrosecondの情報が切り捨てられる...

                yield ModuleMessage(
                    self.module.uuid, self.uuid,
                    timestamp=timestamp, count=row._counter, payload=payload)
