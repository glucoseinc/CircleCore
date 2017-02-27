# -*- coding: utf-8 -*-

"""CircleCoreInfo Model."""

# system module
import datetime
from uuid import UUID

# community module
from six import PY3
import sqlalchemy as sa

# project module
from .base import GUID, UUIDMetaDataBase


if PY3:
    from typing import Dict, Optional


class CcInfo(UUIDMetaDataBase):
    """CircleCoreInfoオブジェクト.

    :param str key_prefix: ストレージキーのプレフィックス
    :param UUID uuid: CcInfo UUID
    :param str display_name: 表示名
    :param bool myself: 自分自身か
    :param Optional[str] work: 所属
    :param Optional[datetime] last_access_time: 最終アクセス時刻
    """
    __tablename__ = 'cc_informations'

    uuid = sa.Column(GUID, primary_key=True)
    display_name = sa.Column(sa.String(255))
    myself = sa.Column(sa.Boolean, nullable=False)
    work = sa.Column(sa.Text, nullable=False)
    created_at = sa.Column(sa.DateTime, nullable=False, default=datetime.datetime.utcnow)

    replication_master_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(
            'replication_masters.replication_master_id',
            name='fk_cc_informations_replication_masters'))

    updated_at = sa.Column(
        sa.DateTime, nullable=False,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow)

    def to_json(self):
        """このモデルのJSON表現を返す.

        :return: json表現のdict
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

    def update_from_json(self, json_msg):
        """JSON表現から更新.

        :param Dict json_msg:
        :rtype: CcInfo
        """
        self.display_name = json_msg.get('displayName', self.display_name)
        self.work = json_msg.get('work', self.work)
