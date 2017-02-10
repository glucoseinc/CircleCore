# -*- coding: utf-8 -*-

"""Module Model."""

# system module
import datetime

# community module
import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy.ext.hybrid import hybrid_property

# project module
from .base import generate_uuid, GUID, UUIDMetaDataBase


class Module(UUIDMetaDataBase):
    """Moduleオブジェクト.

    :param str key_prefix: ストレージキーのプレフィックス
    :param UUID uuid: Module UUID
    :param List[MessageBox] message_boxes: MessageBox
    :param str display_name: 表示名
    :param List[str] tags: タグ
    :param Optional[str] memo: メモ
    """
    __tablename__ = 'modules'

    uuid = sa.Column(GUID, primary_key=True)
    display_name = sa.Column(sa.String(255), nullable=False, default='')
    _tags = sa.Column('_tags', sa.Text, nullable=False, default='')
    memo = sa.Column(sa.Text, nullable=False, default='')
    created_at = sa.Column(sa.DateTime, nullable=False, default=datetime.datetime.utcnow)
    updated_at = sa.Column(
        sa.DateTime, nullable=False,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow)

    message_boxes = orm.relationship('MessageBox', backref='module', cascade='all, delete-orphan')

    def __init__(self, **kwargs):
        """init.
        """

        if 'tags' in kwargs:
            kwargs['_tags'] = ','.join(self.to_tags_list(kwargs.pop('tags')))

        super(Module, self).__init__(**kwargs)

    def __eq__(self, other):
        """return equality.

        :param Module other: other Module
        :return: equality
        :rtype: bool
        """
        return all([self.uuid == other.uuid,
                    self.display_name == other.display_name, self.tags == other.tags,
                    self.memo == other.memo])

    @hybrid_property
    def tags(self):
        return self._tags.split(',') if self._tags is not None else []

    @tags.setter
    def tags(self, tags):
        self._tags = ','.join(self.to_tags_list(tags))

    @classmethod
    def to_tags_list(cls, tags):
        if not tags:
            return []

        if isinstance(tags, str):
            tags = tags.split(',')
        if not isinstance(tags, (list, tuple)):
            raise ValueError('invalid tags type {!r}'.format(tags))
        for tag in tags:
            if ',' in tag:
                raise ValueError('invalid tag, `{}`'.format(tag))
        return tags

    def to_json(self, with_boxes=False, with_schema=False):
        """このモデルのJSON表現を返す.

        :return: json表現のdict
        :rtype: Dict
        """

        d = {
            'uuid': str(self.uuid),
            'messageBoxUuids': [str(box.uuid) for box in self.message_boxes],
            'displayName': self.display_name,
            'tags': [tag for tag in self.tags],
            'memo': self.memo,
        }

        if with_boxes:
            d['messageBoxes'] = [box.to_json(with_schema=with_schema) for box in self.message_boxes]

        return d

    def update_from_json(self, jsonobj, with_boxes=False):
        self.display_name = jsonobj.get('displayName', self.display_name)
        self.tags = jsonobj.get('tags', self.tags)
        self.memo = jsonobj.get('memo', self.memo)

        if with_boxes and 'messageBoxes' in jsonobj:
            from . import MessageBox

            boxes = []
            # TODO: in queryとか使う
            for box_data in jsonobj['messageBoxes']:
                box_uuid = box_data.get('uuid')
                if not box_uuid:
                    print('new module ', box_data)
                    box = MessageBox(
                        uuid=generate_uuid(model=MessageBox),
                        module_uuid=self.uuid,
                        schema_uuid=box_data['schema'],
                        display_name=box_data['displayName'],
                        memo=box_data['memo'],
                    )
                else:
                    box = MessageBox.query.get(box_uuid, )
                    box.update_from_json(box_data)

                boxes.append(box)
                # self.message_boxes.append(box)
            self.message_boxes = boxes

    # @classmethod
    # def from_json(cls, json_msg, **kwargs):
    #     """JSON表現からの復元.

    #     :param dict json_msg:
    #     :rtype: Module
    #     """
    #     return cls(**json_msg, **kwargs)

    # @property
    # def master_uuid(self):
    #     """
    #     :rtype Optional[UUID]:
    #     """
    #     for box_uuid in self.message_box_uuids:
    #         master_uuid = metadata().find_message_box(box_uuid).master_uuid
    #         if master_uuid:
    #             return master_uuid

    #     return None
