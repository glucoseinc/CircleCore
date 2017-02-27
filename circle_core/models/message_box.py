# -*- coding: utf-8 -*-

"""Message Box Model."""

# system module
import datetime

# community module
import sqlalchemy as sa
from sqlalchemy.ext.hybrid import hybrid_property

# project module
from .base import GUID, UUIDMetaDataBase
from .cc_info import CcInfo
from .replication_link import ReplicationLink
from ..utils import prepare_uuid


class MessageBox(UUIDMetaDataBase):
    """MessageBoxオブジェクト

    :param str key_prefix: ストレージキーのプレフィックス
    :param UUID uuid: MessageBox UUID
    :param UUID schema_uuid: Schema UUID
    :param UUID module_uuid: Module UUID
    :param str display_name: 表示名
    :param Optional[str] memo: メモ
    """

    __tablename__ = 'message_boxes'

    uuid = sa.Column(GUID, primary_key=True)
    schema_uuid = sa.Column(GUID, sa.ForeignKey('schemas.uuid'), nullable=False)
    module_uuid = sa.Column(GUID, sa.ForeignKey('modules.uuid'), nullable=False)
    display_name = sa.Column(sa.String(255), nullable=False, default='')
    memo = sa.Column(sa.Text, nullable=False, default='')
    created_at = sa.Column(sa.DateTime, nullable=False, default=datetime.datetime.utcnow)
    updated_at = sa.Column(
        sa.DateTime, nullable=False,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow)

    def __init__(self, **kwargs):
        for key in ('uuid', 'schema_uuid', 'module_uuid'):
            if key in kwargs:
                kwargs[key] = prepare_uuid(kwargs[key])

        super(MessageBox, self).__init__(**kwargs)

    def __hash__(self):
        return hash(self.uuid)

    def __eq__(self, other):
        """return equality.

        :param MessageBox other: other MessageBox
        :return: equality
        :rtype: bool
        """
        return all([self.uuid == other.uuid,
                    self.display_name == other.display_name, self.memo == other.memo])

    @hybrid_property
    def cc_uuid(self):
        return self.module.cc_uuid

    @hybrid_property
    def slave_uuids(self):
        replication_links = [replication_link for replication_link in ReplicationLink.query.all()
                             if self.uuid in [box.uuid for box in replication_link.message_boxes]]
        slave_uuids = set()
        for replication_link in replication_links:
            slave_uuids = slave_uuids.union([slave.slave_uuid for slave in replication_link.slaves])
        return sorted(slave_uuids)

    def to_json(self, with_schema=False, with_module=False, with_slave_cc_infos=False):
        """このモデルのJSON表現を返す.

        :return: json表現のdict
        :rtype: Dict
        """

        d = {
            'uuid': str(self.uuid),
            'displayName': self.display_name,
            'memo': self.memo,
            'moduleUuid': str(self.module_uuid),
            'schemaUuid': str(self.schema_uuid),
        }

        if with_schema:
            d['schema'] = self.schema.to_json()

        if with_module:
            d['module'] = self.module.to_json()

        if with_slave_cc_infos:
            d['slaveCcInfos'] = [cc_info.to_json() for cc_info in
                                 CcInfo.query.filter(CcInfo.uuid.in_(self.slave_uuids)).all()]

        return d

    def update_from_json(self, jsonobj):
        self.display_name = jsonobj.get('displayName', self.display_name)
        self.memo = jsonobj.get('memo', self.memo)
        # assert 'schema' not in jsonobj
        # assert 'schemaUuid' not in jsonobj
        # do not change schema
        if 'schema' in jsonobj:
            # self.schema_uuid = prepare_uuid(jsonobj['schema'])
            assert self.schema_uuid == prepare_uuid(jsonobj['schema'])
        elif 'schemaUuid' in jsonobj:
            # self.schema_uuid = prepare_uuid(jsonobj['schemaUuid'])
            assert self.schema_uuid == prepare_uuid(jsonobj['schemaUuid'])
