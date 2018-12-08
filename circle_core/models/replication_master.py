# -*- coding: utf-8 -*-
"""Replication Master Model."""

# community module
import sqlalchemy as sa
from sqlalchemy import orm

from .base import GUID, MetaDataBase

# type annotation
try:
    from typing import Dict, List, TYPE_CHECKING
    if TYPE_CHECKING:
        from uuid import UUID
        from .cc_info import CcInfo
        from .module import Module
except ImportError:
    pass


class ReplicationMaster(MetaDataBase):
    """ReplicationMasterオブジェクト.
    Slaveに公開するリンクを表現

    :param int id: このオブジェクトの id
    :param str endpoint_url: EndpointのURL
    :param UUID master_uuid: ReplicationMaster UUID
    :param CcInfo info: ReplicationMaster CcInfo
    :param List[Module] modules: Moduleリスト
    """

    __tablename__ = 'replication_masters'

    id = sa.Column('replication_master_id', sa.Integer, primary_key=True)
    endpoint_url = sa.Column(sa.String, unique=True, nullable=False)
    master_uuid = sa.Column(GUID)

    info = orm.relationship(
        'CcInfo', foreign_keys=[master_uuid], primaryjoin='CcInfo.uuid == ReplicationMaster.master_uuid', uselist=False
    )

    modules = orm.relationship('Module', backref='replication_master', cascade='all, delete-orphan')

    def to_json(self):
        """このモデルのJSON表現を返す.

        :return: JSON表現のDict
        :rtype: Dict
        """
        return {
            'id': self.id,
            'endpointUrl': self.endpoint_url,
        }
