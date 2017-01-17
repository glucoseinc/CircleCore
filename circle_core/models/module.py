# -*- coding: utf-8 -*-

"""Module Model."""

# system module
import re
from uuid import UUID

# community module
from six import PY3

from circle_core.utils import prepare_uuid
from ..helpers.metadata import metadata

if PY3:
    from typing import List, Optional, Union


class ModuleError(Exception):
    pass


class Module(object):
    """Moduleオブジェクト.

    :param UUID uuid: Module UUID
    :param List[UUID] message_box_uuids: MessageBox
    :param Optional[str] display_name: 表示名
    :param List[str] tags: タグ
    :param Optional[str] memo: メモ
    """

    def __init__(self, uuid, message_box_uuids, display_name=None, tags=None, memo=None):
        """init.

        :param Union[str, UUID] uuid: Module UUID
        :param List[Union[str, UUID]] message_box_uuids: MessageBoxのUUIDリスト
        :param Optional[str] display_name: 表示名
        :param Optional[str] tags: タグ
        :param Optional[str] memo: メモ
        """
        try:
            uuid = prepare_uuid(uuid)
        except ValueError:
            raise ModuleError('Invalid uuid : {}'.format(uuid))

        _message_box_uuids = []
        for message_box_uuid in message_box_uuids:
            if not isinstance(message_box_uuid, UUID):
                try:
                    message_box_uuid = UUID(message_box_uuid)
                except ValueError:
                    raise ModuleError('Invalid message_box_uuid : {}'.format(message_box_uuids))
            _message_box_uuids.append(message_box_uuid)

        self.uuid = uuid
        self.message_box_uuids = _message_box_uuids
        self.display_name = display_name
        _tags = tags.split(',') if tags is not None else []
        self.tags = [tag for tag in _tags if tag != '']
        self.memo = memo

    def __eq__(self, other):
        """return equality.

        :param Module other: other Module
        :return: equality
        :rtype: bool
        """
        return all([self.uuid == other.uuid, self.message_box_uuids == other.message_box_uuids,
                    self.display_name == other.display_name, self.tags == other.tags,
                    self.memo == other.memo])

    @property
    def stringified_tags(self):
        """タグを文字列化する.

        :return: 文字列化タグ
        :rtype: str
        """
        return ','.join(self.tags)

    @property
    def stringified_message_box_uuids(self):
        """MessageBoxのUUIDリストを文字列化する.

        :return: 文字列化MessageBox UUID
        :rtype: str
        """
        return ','.join([str(uuid) for uuid in self.message_box_uuids])

    @property
    def storage_key(self):
        """ストレージキー.

        :return: ストレージキー
        :rtype: str
        """
        return 'module_{}'.format(self.uuid)

    @classmethod
    def is_key_matched(cls, key):
        """指定のキーがストレージキーの形式にマッチしているか.

        :param str key:
        :return: マッチしているか
        :rtype: bool
        """
        pattern = r'^module_[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$'
        return re.match(pattern, key) is not None

    def to_json(self):
        """このモデルのJSON表現を返す.

        :return: json表現のdict
        :rtype: Dict
        """
        return {
            'uuid': str(self.uuid),
            'message_box_uuids': [str(_uuid) for _uuid in self.message_box_uuids],
            'display_name': self.display_name,
            'tags': [tag for tag in self.tags],
            'memo': self.memo,
        }

    @property
    def of_master(self):
        """
        :return bool:
        """
        return any(metadata().find_message_box(box_uuid).of_master for box_uuid in self.message_box_uuids)
