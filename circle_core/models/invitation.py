# -*- coding: utf-8 -*-
"""Invitation Model."""

# system module
import datetime

# community module
import click
from flask import url_for
import sqlalchemy as sa

# project module
from circle_core.utils import format_date, prepare_date
from .base import GUID, UUIDMetaDataBase

# type annotation
try:
    from typing import Dict, Optional, Union, TYPE_CHECKING
    if TYPE_CHECKING:
        from uuid import UUID
except ImportError:
    pass


class Invitation(UUIDMetaDataBase):
    """User招待オブジェクト.

    :param UUID uuid: Invitation UUID
    :param int max_invites: 最大招待可能人数 0は無制限
    :param int current_invites: 招待済人数
    :param datetime.datetime created_at: 作成日時
    :param datetime.datetime updated_at: 更新日時
    """

    __tablename__ = 'invitations'

    uuid = sa.Column(GUID, primary_key=True)
    max_invites = sa.Column(sa.Integer, nullable=False, default=1)
    current_invites = sa.Column(sa.Integer, nullable=False, default=0)
    created_at = sa.Column(sa.DateTime, nullable=False, default=datetime.datetime.utcnow)
    updated_at = sa.Column(
        sa.DateTime, nullable=False, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow
    )

    __mapper_args__ = {
        'order_by': updated_at.desc(),
    }

    def __init__(self, uuid, max_invites, current_invites=0, created_at=None):
        """init.

        :param Union[str, UUID] uuid: Invitation UUID
        :param int max_invites: 招待可能人数. 0は無制限
        :param int current_invites: 招待済人数
        :param Optional[datetime.datetime] created_at: 作成日時
        """
        if isinstance(max_invites, str):
            max_invites = int(max_invites, 10)
        if max_invites < 0:
            raise ValueError('max_invites must be larger than 0')
        created_at = prepare_date(created_at)
        if created_at and not isinstance(created_at, datetime.datetime):
            raise ValueError('created_at must be datetime.datetime or None, ({!r})'.format(created_at))

        super(Invitation, self).__init__(
            uuid=uuid, max_invites=max_invites, current_invites=current_invites, created_at=created_at
        )

    def can_invite(self):
        """この招待をつかって、さらにユーザを追加できるか.

        :return: 招待可否
        :rtype: bool
        """
        return self.current_invites < self.max_invites

    def inc_invites(self):
        """招待完了数を増加させる."""
        self.current_invites += 1

    @property
    def url(self):
        """このCircleCoreでのInvitationのEndpointのURLを返す.

        :return: URL
        :rtype: str
        """

        def build_url():
            return url_for('public.invitation_endpoint', link_uuid=self.uuid, _external=True)

        try:
            return build_url()
        except RuntimeError:
            flask_app = None
            ctx = click.get_current_context()
            if ctx:
                http_worker = ctx.obj.core.find_worker('http')
                if http_worker:
                    flask_app = http_worker.flask_app

            if flask_app:
                with flask_app.app_context():
                    return build_url()
        return None

    def to_json(self):
        """このモデルのJSON表現を返す.

        :return: JSON表現のDict
        :rtype: Dict
        """
        return {
            'uuid': str(self.uuid),
            'url': self.url,
            'maxInvites': self.max_invites,
            'currentInvites': self.current_invites,
            'createdAt': format_date(self.created_at),
        }

    @classmethod
    def from_json(cls, jsonobj):
        """JSON表現からモデルを生成する.

        :param Dict jsonobj: JSON表現のDict
        :return: User招待オブジェクト
        :rtype: Invitation
        """
        return cls(
            jsonobj['uuid'], jsonobj['maxInvites'], jsonobj.get('currentInvites', 0), jsonobj.get('createdAt', None)
        )
