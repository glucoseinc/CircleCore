# -*- coding: utf-8 -*-

"""Module Model."""

# system module
import datetime
from uuid import UUID

# community module
from six import PY3
import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy.ext.hybrid import hybrid_property

# project module
from .base import generate_uuid, GUID, UUIDMetaDataBase
from .message_box import MessageBox

if PY3:
    from typing import Dict, Iterator, List, Optional, Tuple, Union


class ModuleProperty(object):
    """ModuleProperty.

    :param str name: 属性名
    :param str value: 属性値
    """

    def __init__(self, name_and_value):
        """init.

        :param Union[Dict, str] name_and_value: 属性名と属性値
        """
        if isinstance(name_and_value, str):
            if ':' not in name_and_value:
                raise ValueError('invalid property')
            self.name, self.value = name_and_value.split(':', 1)
        elif isinstance(name_and_value, dict):
            self.name = name_and_value['name']
            self.value = name_and_value['value']

    def __str__(self):
        return '{}:{}'.format(self.name, self.value)

    def to_json(self):
        return {
            'name': self.name,
            'value': self.value
        }


class ModuleProperties(object):
    """ModuleProperties.

    :param List _properties: Properties
    """

    def __init__(self, name_and_values):
        """init.

        :param Union[str, Tuple, List] name_and_values:
        """

        self._properties = []
        if isinstance(name_and_values, str):
            name_and_values = [name_and_value for name_and_value in name_and_values.split(',')
                               if len(name_and_value)]
        if isinstance(name_and_values, (tuple, list)):
            self._properties = [ModuleProperty(name_and_value) for name_and_value in name_and_values]

    def __iter__(self):
        """iter.

        :return: イテレータ
        :rtype: Iterator
        """
        return iter(self._properties)

    def __len__(self):
        """len.

        :return: 長さ
        :rtype: int
        """
        return len(self._properties)

    def __str__(self):
        """str.

        :return: 文字列表現
        :rtype: str
        """
        return ','.join(str(prop) for prop in self._properties)


class Module(UUIDMetaDataBase):
    """Moduleオブジェクト.

    :param UUID uuid: Module UUID
    :param UUID cc_uuid: owner CircleCore UUID
    :param Optional[int] replication_master_id: ReplicationMaster ID
    :param List[MessageBox] message_boxes: MessageBox
    :param str display_name: 表示名
    :param str _properties: 属性
    :param List[ModuleProperties] properties: 属性
    :param str _tags: タグ
    :param List[str] tags: タグ
    :param str memo: メモ
    :param datetime.datetime created_at: 作成日時
    :param datetime.datetime updated_at: 更新日時
    """
    __tablename__ = 'modules'

    uuid = sa.Column(GUID, primary_key=True)
    cc_uuid = sa.Column(GUID, sa.ForeignKey('cc_informations.uuid', name='fk_modules_cc_uuid'), nullable=False)
    replication_master_id = sa.Column(
        sa.Integer, sa.ForeignKey('replication_masters.replication_master_id', name='fk_replication_master_id'))
    display_name = sa.Column(sa.String(255), nullable=False, default='')
    _properties = sa.Column('properties', sa.Text, nullable=False, default='')
    _tags = sa.Column('_tags', sa.Text, nullable=False, default='')
    memo = sa.Column(sa.Text, nullable=False, default='')
    created_at = sa.Column(sa.DateTime, nullable=False, default=datetime.datetime.utcnow)
    updated_at = sa.Column(
        sa.DateTime, nullable=False,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow)

    message_boxes = orm.relationship('MessageBox', backref='module', cascade='all, delete-orphan')

    @classmethod
    def create(cls, **kwargs):
        if 'uuid' not in kwargs:
            kwargs['uuid'] = generate_uuid(model=cls)
        if 'cc_uuid' not in kwargs:
            from .cc_info import CcInfo
            kwargs['cc_uuid'] = CcInfo.query.filter_by(myself=True).one().uuid

        return cls(**kwargs)

    def __init__(self, **kwargs):
        """init.

        :param Dict kwargs: キーワード引数
        """
        if 'properties' in kwargs:
            properties = kwargs['properties']
            if not isinstance(properties, ModuleProperties):
                kwargs['properties'] = ModuleProperties(properties)
        if 'tags' in kwargs:
            kwargs['_tags'] = ','.join(self.to_tags_list(kwargs.pop('tags')))

        super(Module, self).__init__(**kwargs)

    def __hash__(self):
        """hash.

        :return: ハッシュ値
        :rtype: int
        """
        return hash('{}:{!r}'.format(self.__class__.__name__, hash(self.uuid)))

    def __eq__(self, other):
        """eq.

        :param Module other: other Module
        :return: equality
        :rtype: bool
        """
        return all([self.uuid == other.uuid,
                    self.display_name == other.display_name,
                    self.tags == other.tags,
                    self.memo == other.memo])

    @hybrid_property
    def tags(self):
        if self._tags is None or len(self._tags) == 0:
            return []
        return self._tags.split(',')

    @tags.setter
    def tags(self, tags):
        self._tags = ','.join(sorted(set(self.to_tags_list(tags))))

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

    @hybrid_property
    def properties(self):
        return ModuleProperties(self._properties)

    @properties.setter
    def properties(self, properties):
        if not isinstance(properties, ModuleProperties):
            properties = ModuleProperties(properties)
        self._properties = str(properties)

    def to_json(self, with_boxes=False, with_schema=False, with_cc_info=False):
        """このモデルのJSON表現を返す.

        :return: json表現のdict
        :rtype: Dict
        """

        d = {
            'uuid': str(self.uuid),
            'ccUuid': str(self.cc_uuid),
            'messageBoxUuids': [str(box.uuid) for box in self.message_boxes],
            'displayName': self.display_name,
            'tags': [tag for tag in self.tags],
            'properties': [prop.to_json() for prop in self.properties],
            'memo': self.memo,
        }

        if with_boxes:
            d['messageBoxes'] = [box.to_json(with_schema=with_schema, with_slave_cc_infos=with_cc_info)
                                 for box in self.message_boxes]

        if with_cc_info:
            d['ccInfo'] = self.cc_info.to_json()

        return d

    def update_from_json(self, jsonobj, with_boxes=False):
        self.display_name = jsonobj.get('displayName', self.display_name)
        self.tags = jsonobj.get('tags', self.tags)
        if 'properties' in jsonobj:
            self.properties = ModuleProperties(jsonobj['properties'])
        self.memo = jsonobj.get('memo', self.memo)

        if with_boxes and 'messageBoxes' in jsonobj:
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
                    box = MessageBox.query.get(box_uuid)
                    box.update_from_json(box_data)

                boxes.append(box)
                # self.message_boxes.append(box)
            self.message_boxes = boxes
