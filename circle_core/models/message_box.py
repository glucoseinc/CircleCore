# -*- coding: utf-8 -*-

# system module
from datetime import datetime
import re
from time import mktime
from uuid import UUID

# community module
from six import PY3

from .message import ModuleMessage
from ..helpers.metadata import metadata
from ..logger import get_stream_logger
from ..utils import prepare_uuid

if PY3:
    from typing import Optional, Union


logger = get_stream_logger(__name__)


class MessageBoxError(Exception):
    pass


class MessageBox(object):
    """MessageBoxオブジェクト

    :param UUID uuid: MessageBox UUID
    :param UUID schema_uuid: Schema UUID
    :param str display_name: 表示名
    :param Optional[str] memo: メモ
    """
    def __init__(self, uuid, schema_uuid, display_name, memo=None, master_uuid=None):
        """init.

        :param Union[str, UUID] uuid: MessageBox UUID
        :param Union[str, UUID] schema_uuid: Schema UUID
        :param str display_name: 表示名
        :param Optional[str] memo: メモ
        :param Union[NoneType, str, UUID] master_uuid:
        """
        if not isinstance(uuid, UUID):
            try:
                uuid = UUID(uuid)
            except ValueError:
                raise MessageBoxError('Invalid uuid : {}'.format(uuid))

        if not isinstance(schema_uuid, UUID):
            try:
                schema_uuid = UUID(schema_uuid)
            except ValueError:
                raise MessageBoxError('Invalid schema_uuid : {}'.format(schema_uuid))

        self.uuid = uuid
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
    def storage_key(self):
        """ストレージキー.

        :return: ストレージキー
        :rtype: str
        """
        return 'message_box_{}'.format(self.uuid)

    @property
    def module(self):
        for m in metadata().modules:
            for box_uuid in m.message_box_uuids:
                if box_uuid == self.uuid:
                    return m

    @classmethod
    def is_key_matched(cls, key):
        """指定のキーがストレージキーの形式にマッチしているか.

        :param str key:
        :return: マッチしているか
        :rtype: bool
        """
        pattern = r'^message_box_[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$'
        return re.match(pattern, key) is not None

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
