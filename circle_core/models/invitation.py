# -*- coding: utf-8 -*-
"""Invitation Model."""

# system module
import datetime
from typing import Optional, TYPE_CHECKING, Union, cast

# community module
import click

from flask import url_for

import sqlalchemy as sa

# project module
from circle_core.utils import format_date, prepare_date

from .base import GUID, UUIDMetaDataBase

# type annotation
if TYPE_CHECKING:
    from uuid import UUID

    from mypy_extensions import TypedDict

    class InvitationJson(TypedDict, total=True):
        uuid: str
        url: str
        maxInvites: int
        currentInvites: int
        createdAt: Optional[str]


class Invitation(UUIDMetaDataBase):
    """User招待オブジェクト.

    Args:
        uuid: Invitation UUID
        max_invites: 最大招待可能人数 0は無制限
        current_invites: 招待済人数
        created_at: 作成日時
        updated_at: 更新日時
    """
    __tablename__ = 'invitations'

    uuid: 'UUID'
    url: str
    max_invites: int
    current_invites: int
    created_at: datetime.datetime
    updated_at: datetime.datetime

    uuid = sa.Column(GUID, primary_key=True)
    max_invites = sa.Column(sa.Integer, nullable=False, default=1)
    current_invites = sa.Column(sa.Integer, nullable=False, default=0)
    created_at = sa.Column(sa.DateTime, nullable=False, default=datetime.datetime.utcnow)
    updated_at = sa.Column(
        sa.DateTime, nullable=False, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow
    )

    __mapper_args__ = {
        'order_by': updated_at.desc(),  # type: ignore
    }

    def __init__(
        self,
        uuid: 'Union[str, UUID]',
        max_invites: int,
        current_invites: int = 0,
        created_at: Optional[Union[str, datetime.datetime]] = None
    ):
        """init.

        Args:
            uuid: Invitation UUID
            max_invites: 招待可能人数. 0は無制限
            current_invites: 招待済人数
            created_at: 作成日時
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

    def can_invite(self) -> bool:
        """この招待をつかって、さらにユーザを追加できるか.

        :return: 招待可否
        :rtype: bool
        """
        return self.current_invites < self.max_invites

    def inc_invites(self) -> None:
        """招待完了数を増加させる."""
        self.current_invites += 1

    @property
    def url(self) -> Optional[str]:
        """このCircleCoreでのInvitationのEndpointのURLを返す.

        :return: URL
        :rtype: str
        """

        def build_url() -> str:
            return cast(str, url_for('public.invitation_endpoint', link_uuid=self.uuid, _external=True))

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

    def to_json(self) -> 'InvitationJson':
        """このモデルのJSON表現を返す.

        :return: JSON表現のDict
        :rtype: Dict
        """
        return {
            'uuid': str(self.uuid),
            'url': cast(str, self.url),
            'maxInvites': self.max_invites,
            'currentInvites': self.current_invites,
            'createdAt': format_date(self.created_at),
        }

    @classmethod
    def from_json(cls, jsonobj: 'InvitationJson') -> 'Invitation':
        """JSON表現からモデルを生成する.

        Args:
            jsonobj: JSON表現のDict

        Return:
            User招待オブジェクト
        """
        return cls(
            jsonobj['uuid'], jsonobj['maxInvites'], jsonobj.get('currentInvites', 0), jsonobj.get('createdAt', None)
        )
