# -*- coding: utf-8 -*-

"""Replication Link Model."""

# system module
import datetime
from uuid import UUID

# community module
import sqlalchemy as sa
from sqlalchemy import orm

from circle_core.utils import format_date, prepare_date
from .base import GUID, MetaDataBase


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


class ReplicationLink(MetaDataBase):
    """ReplicationLinkオブジェクト.

    :param UUID uuid: ReplicationLink UUID
    :param Optional[str] memo: メモ
    """
    __tablename__ = 'replication_links'

    uuid = sa.Column(GUID, primary_key=True)
    created_at = sa.Column(sa.DateTime, nullable=False, default=datetime.datetime.utcnow)
    updated_at = sa.Column(
        sa.DateTime, nullable=False,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow)

    message_boxes = orm.relationship(
        'MessageBox',
        secondary=replcation_boxes_table,
        backref='links')

    def __init__(self, uuid, message_box_uuids, display_name, memo=None):
        """init.

        :param Union[str, UUID] uuid: Module UUID
        :param List[Union[str, UUID]] message_box_uuids: MessageBoxのUUIDリスト
        :param str display_name: 表示名
        :param Optional[str] memo: メモ
        """
        super(ReplicationLink, self).__init__(uuid, display_name, memo)

        from .message_box import MessageBox

        for message_box_uuid in message_box_uuids:
            if not isinstance(message_box_uuid, UUID):
                try:
                    message_box_uuid = UUID(message_box_uuid)
                except ValueError:
                    raise ValueError('Invalid message_box_uuid : {}'.format(message_box_uuids))
            self.message_boxes.append(MessageBox.query.get(message_box_uuid))

    def __eq__(self, other):
        """return equality.

        :param Module other: other Module
        :return: equality
        :rtype: bool
        """
        return all([self.uuid == other.uuid, self.display_name == other.display_name, self.memo == other.memo])

    def to_json(self):
        """このモデルのJSON表現を返す.

        :return: json表現のdict
        :rtype: Dict
        """
        return {
            'uuid': str(self.uuid),
            'message_box_uuids': [str(_uuid) for _uuid in self.message_box_uuids],
            'display_name': self.display_name,
            'memo': self.memo,
        }
