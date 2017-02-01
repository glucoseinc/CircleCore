# -*- coding: utf-8 -*-

"""CircleCoreInfo Model."""

# system module
from uuid import UUID

# community module
from six import PY3

# project module
from .base import UUIDBasedObject


if PY3:
    from typing import Dict, Union


class CcInfoError(Exception):
    pass


class CcInfo(UUIDBasedObject):
    """CircleCoreInfoオブジェクト.

    :param str key_prefix: ストレージキーのプレフィックス
    :param UUID uuid: CcInfo UUID
    :param str display_name: 表示名
    :param bool myself: 自分自身か
    :param Optional[str] work: 所属
    """

    key_prefix = 'cc_info'

    def __init__(self, uuid, display_name, myself=False, work=None):
        """init.

        :param Union[str, UUID] uuid: CcInfo UUID
        :param str display_name: 表示名
        :param Optional[bool, str] myself: 自分自身か
        :param Optional[str] work: メモ
        """
        super(CcInfo, self).__init__(uuid)

        self.display_name = display_name
        self.myself = myself is True or myself == 'True'
        self.work = work

    def __eq__(self, other):
        """return equality.

        :param CcInfo other: other Schema
        :return: equality
        :rtype: bool
        """
        return all([self.uuid == other.uuid, self.display_name == other.display_name, self.work == other.work])

    def to_json(self):
        """このモデルのJSON表現を返す.

        :return: json表現のdict
        :rtype: Dict
        """
        return {
            'uuid': str(self.uuid),
            'display_name': self.display_name,
            'work': self.work,
            'myself': self.myself,
        }

    @classmethod
    def from_json(cls, json_msg, **kwargs):
        """JSON表現から復元.

        :param Dict json_msg:
        :param Dict kwargs:
        :rtype: CcInfo
        """
        merged_args = {k: v for dic in [json_msg, kwargs] for k, v in dic.items()}
        return CcInfo(**merged_args)