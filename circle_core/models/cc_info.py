# -*- coding: utf-8 -*-
"""CircleCoreInfo Model."""

# system module
import datetime
from typing import List, TYPE_CHECKING

# community module
import sqlalchemy as sa
from sqlalchemy import orm

# project module
from .base import GUID, UUIDMetaDataBase

# type annotation
if TYPE_CHECKING:
    from uuid import UUID

    from .module import Module

    from mypy_extensions import TypedDict

    class CcInfoJson(TypedDict, total=True):
        uuid: str
        displayName: str
        work: str
        myself: str
        lastAccessedAt: str


class CcInfo(UUIDMetaDataBase):
    """CircleCoreInfoオブジェクト.

    Attributes:
        uuid: CcInfo UUID
    :param str display_name: 表示名
    :param bool myself: 自分自身か
    :param str work: 所属
    :param datetime.datetime created_at: 作成日時
    :param datetime.datetime updated_at: 更新日時
    :param int replication_master_id: ReplicationMasterオブジェクトのID
    :param List[Module] modules: Moduleリスト
    """
    uuid: 'UUID'
    modules: 'List[Module]'

    __tablename__ = 'cc_informations'

    uuid = sa.Column(GUID, primary_key=True, unique=True)
    display_name = sa.Column(sa.String(255))
    myself = sa.Column(sa.Boolean, nullable=False)
    work = sa.Column(sa.Text, nullable=False)
    created_at = sa.Column(sa.DateTime, nullable=False, default=datetime.datetime.utcnow)
    updated_at = sa.Column(
        sa.DateTime, nullable=False, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow
    )

    replication_master_id = sa.Column(
        sa.Integer,
        sa.ForeignKey('replication_masters.replication_master_id', name='fk_cc_informations_replication_masters')
    )

    modules = orm.relationship('Module', backref='cc_info')

    def to_json(self) -> 'CcInfoJson':
        """このモデルのJSON表現を返す.

        :return: JSON表現のDict
        :rtype: Dict
        """
        return {
            'uuid': str(self.uuid),
            'displayName': self.display_name,
            'work': self.work,
            'myself': self.myself,
            # TODO: 実装する
            'lastAccessedAt': datetime.datetime.utcnow().isoformat('T') + 'Z',
        }

    def update_from_json(self, jsonobj: 'CcInfoJson') -> None:
        """JSON表現からモデルを更新する.

        :param Dict jsonobj: JSON表現のDict
        """
        self.display_name = jsonobj.get('displayName', self.display_name)
        self.work = jsonobj.get('work', self.work)
