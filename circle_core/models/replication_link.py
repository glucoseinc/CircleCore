# -*- coding: utf-8 -*-

"""Replication Link Model."""

# system module
import datetime
from uuid import UUID

# community module
from flask import current_app, request
import sqlalchemy as sa
from sqlalchemy import orm

from circle_core.utils import format_date, prepare_date, prepare_uuid
from .base import GUID, MetaDataBase, UUIDMetaDataBase


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

    link = orm.relationship(
        'ReplicationLink',
        backref=orm.backref('slaves', cascade='all, delete-orphan'))
    info = orm.relationship(
        'CcInfo', foreign_keys=[slave_uuid], primaryjoin='CcInfo.uuid == ReplicationSlave.slave_uuid', uselist=False)


class ReplicationLink(UUIDMetaDataBase):
    """ReplicationLinkオブジェクト.
    Slaveに公開するリンクを表現

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
    def create(cls, display_name, memo, message_box_uuids):
        """ReplicationLinkを作成する。
        message boxの存在チェックとかを行う

        :param str display_name: 表示名
        :param Optional[str] memo: メモ
        :param Union[ALL_MESSAGE_BOXES, List[Union[str, UUID]]] message_box_uuids: MessageBoxのUUIDリスト
        """
        from . import generate_uuid, MessageBox

        obj = ReplicationLink(
            uuid=generate_uuid(model=cls),
            display_name=display_name,
            memo=memo,
        )

        if message_box_uuids is cls.ALL_MESSAGE_BOXES:
            query = MessageBox.query
        else:
            if not message_box_uuids:
                raise ValueError('no box specified')
            query = MessageBox.query.filter(MessageBox.uuid.in_(message_box_uuids))
        obj.message_boxes = query.all()

        return obj

    def __init__(self, **kwargs):
        """init.
        """
        super(ReplicationLink, self).__init__(**kwargs)

    def __eq__(self, other):
        """return equality.

        :param Module other: other Module
        :return: equality
        :rtype: bool
        """
        return all([self.uuid == other.uuid, self.display_name == other.display_name, self.memo == other.memo])

    @property
    def link(self):
        """このCircleCoreでの共有リンクのEndpointのURLを返す"""
        def build_link():
            return 'ws://{server_name}:{port}/replication/{_uuid}'.format(
                server_name=request.environ['SERVER_NAME'],
                port=current_app.ws_port or request.environ['SERVER_PORT'],
                _uuid=self.uuid
            )

        try:
            return build_link()
        except RuntimeError:
            import click

            flask_app = None
            ctx = click.get_current_context()
            if ctx:
                http_worker = ctx.obj.core.find_worker('http')
                if http_worker:
                    flask_app = http_worker.flask_app

            if flask_app:
                with flask_app.test_request_context('/'):
                    return build_link()
        return None

    def to_json(self, with_slaves=False, with_boxes=False, with_module=True, with_schema=True):
        """このモデルのJSON表現を返す.

        :return: json表現のdict
        :rtype: Dict
        """

        slaves = []
        for slave in self.slaves:
            if with_slaves and slave.info:
                slaves.append(slave.info.to_json())
            else:
                slaves.append(dict(uuid=slave.slave_uuid))

        message_boxes = []
        # modules = {}
        for box in self.message_boxes:
            if with_boxes:
                message_boxes.append(box.to_json(with_module=with_module, with_schema=with_schema))
            else:
                message_boxes.append(dict(uuid=box.uuid))

        d = {
            'uuid': str(self.uuid),
            # 'ccInfoUuids': [str(_uuid) for _uuid in self.cc_info_uuids],
            # 'messageBoxUuids': [str(_uuid) for _uuid in self.message_box_uuids],
            'displayName': self.display_name,
            'memo': self.memo,
            'link': self.link,
            'slaves': slaves,
            'messageBoxes': message_boxes,
        }
        if d['link'] is None:
            d.pop('link')

        return d
