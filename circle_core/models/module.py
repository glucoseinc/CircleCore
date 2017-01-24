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
        :param Union[Optional[str], List[str]] tags: タグ
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
        self.memo = memo

        if tags is None:
            _tags = []
        elif isinstance(tags, list):
            _tags = tags
        else:
            _tags = tags.split(',')
        _tags = [tag for tag in _tags if tag != '']     # 空白除去
        _tags = sorted(set(_tags), key=_tags.index)     # 重複除去
        self.tags = _tags

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

    @classmethod
    def from_json(cls, json_msg, **kwargs):
        """JSON表現からの復元.

        :param dict json_msg:
        :rtype: Module
        """
        return cls(**json_msg, **kwargs)

    @property
    def master_uuid(self):
        """
        :rtype Optional[UUID]:
        """
        for box_uuid in self.message_box_uuids:
            master_uuid = metadata().find_message_box(box_uuid).master_uuid
            if master_uuid:
                return master_uuid

        return None
