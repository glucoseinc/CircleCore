# -*- coding: utf-8 -*-

"""User Model."""

# system module
import datetime

# community module
import sqlalchemy as sa

from circle_core.utils import format_date, prepare_date
from .base import GUID, UUIDMetaDataBase


class Invitation(UUIDMetaDataBase):
    """User招待オブジェクト.

    :param str key_prefix: ストレージキーのプレフィックス
    :param UUID uuid: User UUID
    :param int max_invites: 最大招待可能人数. 0は無制限
    :param int current_invites: 招待済人数.
    :param datetime.datetime created_at: 招待作成日 なければNone
    """
    __tablename__ = 'invitations'

    uuid = sa.Column(GUID, primary_key=True)
    max_invites = sa.Column(sa.Integer, nullable=False, default=1)
    current_invites = sa.Column(sa.Integer, nullable=False, default=0)
    created_at = sa.Column(sa.DateTime, nullable=False, default=datetime.datetime.utcnow)
    updated_at = sa.Column(
        sa.DateTime, nullable=False,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow)

    def __init__(self, uuid, max_invites, created_at=None, current_invites=0):
        """init.

        :param Union[str, UUID] uuid: User UUID
        :param int max_invites: 招待可能人数. 0は無制限
        :param datetime.datetime created_at: 招待作成日 なければNone
        """
        if isinstance(max_invites, str):
            max_invites = int(max_invites, 10)
        if max_invites < 0:
            raise ValueError('max_invites must be larger than 0')
        created_at = prepare_date(created_at)
        if created_at and not isinstance(created_at, datetime.datetime):
            raise ValueError('created_at must be datetime.datetime or None, ({!r})'.format(created_at))

        super(Invitation, self).__init__(
            uuid=uuid, max_invites=max_invites, created_at=created_at, current_invites=current_invites)

    def to_json(self):
        """このモデルのJSON表現を返す.

        :return: json表現のdict
        :rtype: Dict
        """
        return {
            'uuid': str(self.uuid),
            'maxInvites': self.max_invites,
            'currentInvites': self.current_invites,
            'createdAt': format_date(self.created_at)
        }

    @classmethod
    def from_json(cls, jsonobj):
        """JSON表現からモデルを生成する.

        :param jsonobj: json表現のdict
        :return: User招待オブジェクト.
        :rtype: Invitation
        """
        return cls(jsonobj['uuid'], jsonobj['maxInvites'], jsonobj['createdAt'])
