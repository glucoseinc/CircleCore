# -*- coding: utf-8 -*-

"""User Model."""

# system module
import datetime
from uuid import UUID

# community module
from six import PY3

from circle_core.utils import format_date, prepare_date
from .base import UUIDBasedObject

if PY3:
    from typing import Union


class Invitation(UUIDBasedObject):
    """User招待オブジェクト.

    :param str key_prefix: ストレージキーのプレフィックス
    :param UUID uuid: User UUID
    :param int max_invites: 招待可能人数. 0は無制限
    :param datetime.datetime date_created: 招待作成日 なければNone
    """

    key_prefix = 'invitation'

    def __init__(self, uuid, max_invites, date_created=None, current_invites=0):
        """init.

        :param Union[str, UUID] uuid: User UUID
        :param int max_invites: 招待可能人数. 0は無制限
        :param datetime.datetime date_created: 招待作成日 なければNone
        """
        super(Invitation, self).__init__(uuid)

        if isinstance(max_invites, str):
            max_invites = int(max_invites, 10)
        if max_invites < 0:
            raise ValueError('max_invites must be larger than 0')
        date_created = prepare_date(date_created)
        if date_created and not isinstance(date_created, datetime.datetime):
            raise ValueError('date_created must be datetime.datetime or None, ({!r})'.format(date_created))

        self.max_invites = max_invites
        self.current_invites = current_invites
        self.date_created = date_created

    def to_json(self):
        """このモデルのJSON表現を返す.

        :return: json表現のdict
        :rtype: Dict
        """
        return {
            'uuid': str(self.uuid),
            'maxInvites': self.max_invites,
            'currentInvites': self.current_invites,
            'dateCreated': format_date(self.date_created)
        }

    @classmethod
    def from_json(cls, jsonobj):
        """JSON表現からモデルを生成する.

        :param jsonobj: json表現のdict
        :return: User招待オブジェクト.
        :rtype: Invitation
        """
        return cls(jsonobj['uuid'], jsonobj['maxInvites'], jsonobj['dateCreated'])
