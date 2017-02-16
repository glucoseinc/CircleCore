# -*- coding: utf-8 -*-

"""Replication Link Model."""

# system module
import datetime
from uuid import UUID

# community module
from flask import url_for
import sqlalchemy as sa
from sqlalchemy import orm

# from circle_core.utils import format_date, prepare_date, prepare_uuid
from .base import GUID, MetaDataBase


class ReplicationMaster(MetaDataBase):
    """ReplicationMasterオブジェクト.
    Slaveに公開するリンクを表現

    :param int id: object's id
    """
    __tablename__ = 'replication_masters'

    id = sa.Column('replication_master_id', sa.Integer, primary_key=True)
    endpoint_url = sa.Column(sa.String, unique=True, nullable=False)
    master_uuid = sa.Column(GUID)
    # created_at = sa.Column(sa.DateTime, nullable=False, default=datetime.datetime.utcnow)

    info = orm.relationship(
        'CcInfo', foreign_keys=[master_uuid], primaryjoin='CcInfo.uuid == ReplicationMaster.master_uuid', uselist=False)

    def to_json(self):
        return {
            'id': self.id,
            'endpointUrl': self.endpoint_url,
        }
