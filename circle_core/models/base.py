# -*- coding: utf-8 -*-

"""Model Base."""

# system module
import re
from uuid import UUID

# community module
from six import PY3

if PY3:
    from typing import Union


class UUIDBasedObject(object):
    """UUIDを持つ基底オブジェクト.
    :param str key_prefix: ストレージキーのプレフィックス
    :param UUID uuid: Object UUID
    """

    key_prefix = ''

    def __init__(self, uuid):
        """init.

        :param Union[str, UUID] uuid: User UUID
        """
        if uuid and not isinstance(uuid, UUID):
            try:
                uuid = UUID(uuid)
            except ValueError:
                raise ValueError('Invalid uuid : {}'.format(uuid))

        self.uuid = uuid

    @classmethod
    def make_storage_key(cls, uuid):
        """ストレージキーを作成する.

        :param UUID uuid: UUID
        :return: ストレージキー
        :rtype: str
        """
        return '{}_{}'.format(cls.key_prefix, uuid)

    @property
    def storage_key(self):
        """ストレージキー.

        :return: ストレージキー
        :rtype: str
        """
        return self.make_storage_key(self.uuid)

    @classmethod
    def is_key_matched(cls, key):
        """指定のキーがストレージキーの形式にマッチしているか.

        :param str key:
        :return: マッチしているか
        :rtype: bool
        """
        pattern = '^{}_{}'.format(
            cls.key_prefix,
            r'[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$'
        )
        return re.match(pattern, key) is not None
