# -*- coding: utf-8 -*-

"""Replication Link Model."""

# system module
import datetime
from uuid import UUID

# community module
import sqlalchemy as sa
from sqlalchemy import orm

from circle_core.utils import format_date, prepare_date, prepare_uuid
from .base import GUID, MetaDataBase, UUIDList, UUIDMetaDataBase


replcation_boxes_table = sa.Table(
    'replication_boxes', MetaDataBase.metadata,
    sa.Column('link_uuid', GUID, sa.ForeignKey('replication_links.uuid')),
    sa.Column('box_uuid', GUID, sa.ForeignKey('message_boxes.uuid')),
)


class ReplicationSlave(MetaDataBase):
    __tablename__ = 'replication_slaves'
    __table_args__ = (
        sa.PrimaryKeyConstraint('link_uuid', 'slave_uuid', name='replication_slaves_pk'),
    )

    link_uuid = sa.Column(GUID, sa.ForeignKey('replication_links.uuid'), nullable=False)
    slave_uuid = sa.Column(GUID, nullable=False)
    last_access_at = sa.Column(sa.DateTime)

    link = orm.relationship('ReplicationLink', backref='slaves')
    info = orm.relationship(
        'CcInfo', foreign_keys=[slave_uuid], primaryjoin='CcInfo.uuid == ReplicationSlave.slave_uuid', uselist=False)


class ReplicationLink(UUIDMetaDataBase):
    """ReplicationLinkオブジェクト.

    :param UUID uuid: ReplicationLink UUID
    :param str display_name: 表示名
    :param List[UUID] cc_info_uuids: CircleCoreInfo
    :param List[UUID] message_box_uuids: MessageBox
    :param Optional[str] memo: メモ
    """
    __tablename__ = 'replication_links'

    uuid = sa.Column(GUID, primary_key=True)
    display_name = sa.Column(sa.String(255), nullable=False, default='')
    memo = sa.Column(sa.Text, nullable=False, default='')
    target_cores = sa.Column(UUIDList, nullable=False, default=[])
    created_at = sa.Column(sa.DateTime, nullable=False, default=datetime.datetime.utcnow)
    updated_at = sa.Column(
        sa.DateTime, nullable=False,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow)

    message_boxes = orm.relationship(
        'MessageBox',
        secondary=replcation_boxes_table,
        backref='links')

    ALL_MESSAGE_BOXES = object()

    @classmethod
    def create(cls, display_name, memo, target_cores, message_box_uuids):
        """ReplicationLinkを作成する。
        message boxの存在チェックとかを行う

        :param Union[str, UUID] uuid: Module UUID
        :param str display_name: 表示名
        :param Optional[str] memo: メモ
        :param List[Union[str, UUID]] target_cores: CircleCoreInfoのUUIDリスト
        :param Union[ALL_MESSAGE_BOXES, List[Union[str, UUID]]] message_box_uuids: MessageBoxのUUIDリスト
        """
        from . import generate_uuid, MessageBox

        obj = ReplicationLink(
            uuid=generate_uuid(model=cls),
            display_name=display_name,
            memo=memo,
            target_cores=target_cores,
        )

        if message_box_uuids is cls.ALL_MESSAGE_BOXES:
            query = MessageBox.query
        else:
            if not message_box_uuids:
                raise ValueError('no box specified')
            query = MessageBox.query.filter(MessageBox.uuid.in_(message_box_uuids))
        obj.message_boxes = list(box.uuid for box in query)

        return obj

    def __init__(self, **kwargs):
        """init.

        :param Union[str, UUID] uuid: Module UUID
        :param List[Union[str, UUID]] target_cores: CircleCoreInfoのUUIDリスト
        :param List[Union[str, UUID]] message_box_uuids: MessageBoxのUUIDリスト
        :param str display_name: 表示名
        :param Optional[str] memo: メモ
        """
        if 'target_cores' in kwargs:
            kwargs['target_cores'] = list(prepare_uuid(x) for x in kwargs['target_cores'])

        super(ReplicationLink, self).__init__(**kwargs)

    def __eq__(self, other):
        """return equality.

        :param Module other: other Module
        :return: equality
        :rtype: bool
        """
        return all([self.uuid == other.uuid, self.display_name == other.display_name, self.memo == other.memo])

    # @property
    # def stringified_cc_info_uuids(self):
    #     """CircleCoreInfoのUUIDリストを文字列化する.

    #     :return: 文字列化CircleCoreInfo UUID
    #     :rtype: str
    #     """
    #     return ','.join([str(uuid) for uuid in self.cc_info_uuids])

    # @property
    # def stringified_message_box_uuids(self):
    #     """MessageBoxのUUIDリストを文字列化する.

    #     :return: 文字列化MessageBox UUID
    #     :rtype: str
    #     """
    #     return ','.join([str(uuid) for uuid in self.message_box_uuids])

    def to_json(self):
        """このモデルのJSON表現を返す.

        :return: json表現のdict
        :rtype: Dict
        """
        return {
            'uuid': str(self.uuid),
            # 'ccInfoUuids': [str(_uuid) for _uuid in self.cc_info_uuids],
            # 'messageBoxUuids': [str(_uuid) for _uuid in self.message_box_uuids],
            'displayName': self.display_name,
            'memo': self.memo,
        }
