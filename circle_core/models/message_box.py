# -*- coding: utf-8 -*-

# system module
import re
from uuid import UUID

# community module
from six import PY3

if PY3:
    from typing import Optional, Union


class MessageBoxError(Exception):
    pass


class MessageBox(object):
    """MessageBoxオブジェクト

    :param UUID uuid: MessageBox UUID
    :param UUID schema_uuid: Schema UUID
    :param Optional[str] display_name: 表示名
    :param Optional[str] description: 説明
    """
    def __init__(self, uuid, schema_uuid, display_name=None, description=None):
        """init.

        :param Union[str, UUID] uuid: MessageBox UUID
        :param Union[str, UUID] schema_uuid: Schema UUID
        :param Optional[str] display_name: 表示名
        :param Optional[str] description: 説明
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

    @property
    def storage_key(self):
        """ストレージキー.

        :return: ストレージキー
        :rtype: str
        """
        return 'message_box_{}'.format(self.uuid)

    @classmethod
    def is_key_matched(cls, key):
        """指定のキーがストレージキーの形式にマッチしているか.

        :param str key:
        :return: マッチしているか
        :rtype: bool
        """
        pattern = r'^message_box_[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$'
        return re.match(pattern, key) is not None
