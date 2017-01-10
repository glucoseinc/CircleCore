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

if PY3:
    from typing import Optional, Union


logger = get_stream_logger(__name__)


class MessageBoxError(Exception):
    pass


class MessageBox(object):
    """MessageBoxオブジェクト

    :param UUID uuid: MessageBox UUID
    :param UUID schema_uuid: Schema UUID
    :param Optional[str] display_name: 表示名
    :param Optional[str] description: 説明
    """
    def __init__(self, uuid, schema_uuid, display_name=None, description=None, of_master=False):
        """init.

        :param Union[str, UUID] uuid: MessageBox UUID
        :param Union[str, UUID] schema_uuid: Schema UUID
        :param Optional[str] display_name: 表示名
        :param Optional[str] description: 説明
        :param Bool of_master:
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
        self.description = description
        self.of_master = of_master

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

    def serialize(self):
        """このインスタンスをslaveが再構築できるだけの情報.

        レプリケーション時に使用.
        """
        return {
            'uuid': self.uuid.hex,
            'schema_uuid': self.schema_uuid.hex,
            'display_name': self.display_name,
            'description': self.description
        }

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
            created_at = datetime.fromtimestamp(timestamp)  # TODO: Python側ではdatetimeを使うよう統一
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
                timestamp = row._created_at.timestamp()  # timetupleを使うとmicrosecondの情報が切り捨てられる...

                yield ModuleMessage(self.module.uuid, payload=payload, timestamp=timestamp, count=row._counter)
