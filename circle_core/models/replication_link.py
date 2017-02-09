# -*- coding: utf-8 -*-

"""Replication Link Model."""

# system module
from uuid import UUID

# community module
from six import PY3

# project module
from .base import UUIDBasedObject

if PY3:
    from typing import List, Optional, Union


class ReplicationLinkError(Exception):
    pass


class ReplicationLink(UUIDBasedObject):
    """ReplicationLinkオブジェクト.

    :param str key_prefix: ストレージキーのプレフィックス
    :param UUID uuid: ReplicationLink UUID
    :param str display_name: 表示名
    :param List[UUID] cc_info_uuids: CircleCoreInfo
    :param List[UUID] message_box_uuids: MessageBox
    :param Optional[str] memo: メモ
    """

    key_prefix = 'replication_link'

    def __init__(self, uuid, cc_info_uuids, message_box_uuids, display_name, memo=None):
        """init.

        :param Union[str, UUID] uuid: Module UUID
        :param List[Union[str, UUID]] cc_info_uuids: CircleCoreInfoのUUIDリスト
        :param List[Union[str, UUID]] message_box_uuids: MessageBoxのUUIDリスト
        :param str display_name: 表示名
        :param Optional[str] memo: メモ
        """
        super(ReplicationLink, self).__init__(uuid)

        _cc_info_uuids = []
        for cc_info_uuid in cc_info_uuids:
            if not isinstance(cc_info_uuid, UUID):
                try:
                    cc_info_uuid = UUID(cc_info_uuid)
                except ValueError:
                    raise ReplicationLinkError('Invalid cc_info_uuid : {}'.format(cc_info_uuids))
            _cc_info_uuids.append(cc_info_uuid)

        _message_box_uuids = []
        for message_box_uuid in message_box_uuids:
            if not isinstance(message_box_uuid, UUID):
                try:
                    message_box_uuid = UUID(message_box_uuid)
                except ValueError:
                    raise ReplicationLinkError('Invalid message_box_uuid : {}'.format(message_box_uuids))
            _message_box_uuids.append(message_box_uuid)

        self.cc_info_uuids = _cc_info_uuids
        self.message_box_uuids = _message_box_uuids
        self.display_name = display_name
        self.memo = memo

    def __eq__(self, other):
        """return equality.

        :param Module other: other Module
        :return: equality
        :rtype: bool
        """
        return all([self.uuid == other.uuid, self.display_name == other.display_name, self.memo == other.memo])

    @property
    def stringified_cc_info_uuids(self):
        """CircleCoreInfoのUUIDリストを文字列化する.

        :return: 文字列化CircleCoreInfo UUID
        :rtype: str
        """
        return ','.join([str(uuid) for uuid in self.cc_info_uuids])

    @property
    def stringified_message_box_uuids(self):
        """MessageBoxのUUIDリストを文字列化する.

        :return: 文字列化MessageBox UUID
        :rtype: str
        """
        return ','.join([str(uuid) for uuid in self.message_box_uuids])

    def to_json(self):
        """このモデルのJSON表現を返す.

        :return: json表現のdict
        :rtype: Dict
        """
        return {
            'uuid': str(self.uuid),
            'cc_info_uuids': [str(_uuid) for _uuid in self.cc_info_uuids],
            'message_box_uuids': [str(_uuid) for _uuid in self.message_box_uuids],
            'display_name': self.display_name,
            'memo': self.memo,
        }
