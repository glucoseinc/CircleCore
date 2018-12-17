# -*- coding: utf-8 -*-
"""Replication Master Model."""

from typing import List, TYPE_CHECKING

# community module
import sqlalchemy as sa
from sqlalchemy import orm

from .base import GUID, MetaDataBase

# type annotation
if TYPE_CHECKING:
    from uuid import UUID

    from mypy_extensions import TypedDict

    from .cc_info import CcInfo
    from .module import Module

    class ReplicationMasterJson(TypedDict, total=True):
        id: int
        endpointUrl: str


class ReplicationMaster(MetaDataBase):
    """ReplicationMasterオブジェクト.
    Slaveに公開するリンクを表現

    Args:
        endpoint_url: EndpointのURL
        id: このオブジェクトの id
        info: ReplicationMaster CcInfo
        master_uuid: ReplicationMaster UUID
        modules: Moduleリスト
    """
    endpoint_url: str
    id: int
    info: 'CcInfo'
    master_uuid: 'UUID'
    module: 'List[Module]'

    __tablename__ = 'replication_masters'

    id = sa.Column('replication_master_id', sa.Integer, primary_key=True)
    endpoint_url = sa.Column(sa.String, unique=True, nullable=False)
    master_uuid = sa.Column(GUID)

    info = orm.relationship(
        'CcInfo', foreign_keys=[master_uuid], primaryjoin='CcInfo.uuid == ReplicationMaster.master_uuid', uselist=False
    )

    modules = orm.relationship('Module', backref='replication_master', cascade='all, delete-orphan')

    def to_json(self) -> 'ReplicationMasterJson':
        """このモデルのJSON表現を返す.

        :return: JSON表現のDict
        :rtype: Dict
        """
        return {
            'id': self.id,
            'endpointUrl': self.endpoint_url,
        }
