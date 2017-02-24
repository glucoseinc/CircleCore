# -*- coding: utf-8 -*-

"""Message Box Model."""

# system module
import datetime

# community module
import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy.ext.hybrid import hybrid_property

# project module
from .base import GUID, UUIDMetaDataBase
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

    def to_json(self, with_schema=False, with_module=False):
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
