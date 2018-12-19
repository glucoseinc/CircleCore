# -*- coding: utf-8 -*-
"""Message Box Model."""

# system module
import datetime
from typing import Any, List, MutableSet, Optional, TYPE_CHECKING

# community module
import sqlalchemy as sa
from sqlalchemy.ext.hybrid import hybrid_property

# project module
from .base import GUID, UUIDMetaDataBase
from .replication_link import ReplicationLink
from ..utils import prepare_uuid

# type annotation

if TYPE_CHECKING:
    from uuid import UUID

    from mypy_extensions import TypedDict

    from .cc_info import CcInfoJson
    from .module import Module, ModuleJson
    from .schema import SchemaJson

    class MessageBoxJson(TypedDict, total=False):
        uuid: str
        displayName: str
        memo: str
        moduleUuid: str
        schemaUuid: str
        schema: Optional[SchemaJson]
        module: Optional[ModuleJson]
        slaveCcInfos: Optional[List[CcInfoJson]]


class MessageBox(UUIDMetaDataBase):
    """MessageBoxオブジェクト.

    :param UUID uuid: MessageBox UUID
    :param UUID schema_uuid: Schema UUID
    :param UUID schema_uuid: Schema UUID
    :param Module module: Module
    :param str display_name: 表示名
    :param str memo: メモ
    :param datetime.datetime created_at: 作成日時
    :param datetime.datetime updated_at: 更新日時
    """
    uuid: 'UUID'
    schema_uuid: 'UUID'
    module: 'Module'
    module_uuid: 'UUID'
    display_name: str
    memo: str
    created_at: datetime.datetime
    updated_at: datetime.datetime

    __tablename__ = 'message_boxes'

    uuid = sa.Column(GUID, primary_key=True)
    schema_uuid = sa.Column(GUID, sa.ForeignKey('schemas.uuid'), nullable=False)
    module_uuid = sa.Column(GUID, sa.ForeignKey('modules.uuid'), nullable=False)
    display_name = sa.Column(sa.String(255), nullable=False, default='')
    memo = sa.Column(sa.Text, nullable=False, default='')
    created_at = sa.Column(sa.DateTime, nullable=False, default=datetime.datetime.utcnow)
    updated_at = sa.Column(
        sa.DateTime, nullable=False, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow
    )

    def __init__(self, **kwargs: Any):
        """init.

        :param Dict kwargs: キーワード引数
        """
        for key in ('uuid', 'schema_uuid', 'module_uuid'):
            if key in kwargs:
                kwargs[key] = prepare_uuid(kwargs[key])

        super(MessageBox, self).__init__(**kwargs)

    def __hash__(self) -> int:
        """hash.

        Return:
            ハッシュ値
        """
        return hash(self.uuid)

    def __eq__(self, other: Any) -> bool:
        """eq.

        Args:
            other: other MessageBox
        Return:
            equality
        """
        if not isinstance(other, MessageBox):
            return False
        return all([self.uuid == other.uuid, self.display_name == other.display_name, self.memo == other.memo])

    @hybrid_property
    def cc_uuid(self) -> 'UUID':
        """CCInfo UUIDを返す.

        :return: owner CircleCore UUID
        :rtype: UUID
        """
        return self.module.cc_uuid

    @hybrid_property
    def slave_uuids(self) -> 'List[UUID]':
        """ReplicationSlaveのUUIDリストを返す.

        :return: ReplicationSlave CcInfo UUIDリスト
        :rtype: List[UUID]
        """
        replication_links = [
            replication_link for replication_link in ReplicationLink.query.all()
            if self.uuid in [box.uuid for box in replication_link.message_boxes]
        ]
        slave_uuids: MutableSet[UUID] = set()
        for replication_link in replication_links:
            slave_uuids |= set([slave.slave_uuid for slave in replication_link.slaves])
        return sorted(slave_uuids)

    def to_json(
        self, with_schema: bool = False, with_module: bool = False, with_slave_cc_infos: bool = False
    ) -> 'MessageBoxJson':
        """このモデルのJSON表現を返す.

        :param bool with_schema: 返り値にSchemaの情報を含めるか
        :param bool with_module: 返り値にModuleの情報を含めるか
        :param bool with_slave_cc_infos: 返り値にReplicationSlavesの情報を含めるか
        :return: JSON表現のDict
        :rtype: Dict
        """
        d: 'MessageBoxJson' = {
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
            from .cc_info import CcInfo

            query = CcInfo.query.filter(CcInfo.uuid.in_(self.slave_uuids)).all()  # type: ignore
            d['slaveCcInfos'] = [cc_info.to_json() for cc_info in query]

        return d

    def update_from_json(self, jsonobj) -> None:
        """JSON表現からモデルを更新する.

        :param Dict jsonobj: JSON表現のDict
        """
        self.display_name = jsonobj.get('displayName', self.display_name)
        self.memo = jsonobj.get('memo', self.memo)
        # do not change schema
        if 'schema' in jsonobj:
            assert self.schema_uuid == prepare_uuid(jsonobj['schema'])
        elif 'schemaUuid' in jsonobj:
            assert self.schema_uuid == prepare_uuid(jsonobj['schemaUuid'])
