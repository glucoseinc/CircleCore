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
from .message_box import MessageBox


# type annotation
try:
    from typing import Dict, Iterator, List, Optional, Tuple, Union, TYPE_CHECKING
    if TYPE_CHECKING:
        from uuid import UUID
except ImportError:
    pass


class ModuleAttribute(object):
    """ModuleAttribute.

    :param str name: 属性名
    :param str value: 属性値
    """

    def __init__(self, name_and_value):
        """init.

        :param Union[Dict, str] name_and_value: 属性名と属性値
        """
        if isinstance(name_and_value, str):
            if ':' not in name_and_value:
                raise ValueError('invalid attribute')
            self.name, self.value = name_and_value.split(':', 1)
        elif isinstance(name_and_value, dict):
            self.name = name_and_value['name']
            self.value = name_and_value['value']

    def __str__(self):
        """str.

        :return: 文字列表現
        :rtype: str
        """
        return '{}:{}'.format(self.name, self.value)

    def to_json(self):
        """このモデルのJSON表現を返す.

        :return: JSON表現のDict
        :rtype: Dict
        """
        return {
            'name': self.name,
            'value': self.value
        }


class ModuleAttributes(object):
    """ModuleAttributes.

    :param List[ModuleAttribute] _attributes: ModuleAttributeリスト
    """

    def __init__(self, name_and_values):
        """init.

        :param Union[str, Tuple, List] name_and_values: 属性名と属性値
        """

        self._attributes = []
        if isinstance(name_and_values, str):
            name_and_values = [name_and_value for name_and_value in name_and_values.split(',')
                               if len(name_and_value)]
        if isinstance(name_and_values, (tuple, list)):
            self._attributes = [ModuleAttribute(name_and_value) for name_and_value in name_and_values]

    def __iter__(self):
        """iter.

        :return: イテレータ
        :rtype: Iterator
        """
        return iter(self._attributes)

    def __len__(self):
        """len.

        :return: 長さ
        :rtype: int
        """
        return len(self._attributes)

    def __str__(self):
        """str.

        :return: 文字列表現
        :rtype: str
        """
        return ','.join(str(attribute) for attribute in self._attributes)


class Module(UUIDMetaDataBase):
    """Moduleオブジェクト.

    :param UUID uuid: Module UUID
    :param UUID cc_uuid: owner CircleCore UUID
    :param Optional[int] replication_master_id: ReplicationMaster ID
    :param str display_name: 表示名
    :param str _attributes: 属性
    :param List[ModuleAttributes] attributes: 属性
    :param str _tags: タグ
    :param List[str] tags: タグ
    :param str memo: メモ
    :param datetime.datetime created_at: 作成日時
    :param datetime.datetime updated_at: 更新日時
    :param List[MessageBox] message_boxes: MessageBox
    """

    __tablename__ = 'modules'

    uuid = sa.Column(GUID, primary_key=True)
    cc_uuid = sa.Column(GUID, sa.ForeignKey('cc_informations.uuid', name='fk_modules_cc_uuid'), nullable=False)
    replication_master_id = sa.Column(
        sa.Integer, sa.ForeignKey('replication_masters.replication_master_id', name='fk_replication_master_id'))
    display_name = sa.Column(sa.String(255), nullable=False, default='')
    _attributes = sa.Column('attributes', sa.Text, nullable=False, default='')
    _tags = sa.Column('_tags', sa.Text, nullable=False, default='')
    memo = sa.Column(sa.Text, nullable=False, default='')
    created_at = sa.Column(sa.DateTime, nullable=False, default=datetime.datetime.utcnow)
    updated_at = sa.Column(sa.DateTime, nullable=False, default=datetime.datetime.utcnow,
                           onupdate=datetime.datetime.utcnow)

    message_boxes = orm.relationship('MessageBox', backref='module', cascade='all, delete-orphan')

    @classmethod
    def create(cls, **kwargs):
        """このモデルを作成する.

        :param Dict kwargs: キーワード引数
        :return: Moduleオブジェクト
        :rtype: Module
        """
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
        if 'attributes' in kwargs:
            attributes = kwargs['attributes']
            if not isinstance(attributes, ModuleAttributes):
                kwargs['attributes'] = ModuleAttributes(attributes)
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
        """タグリストを返す.

        :return: タグリスト
        :rtype: List[str]
        """
        if self._tags is None or len(self._tags) == 0:
            return []
        return self._tags.split(',')

    @tags.setter  # type: ignore
    def tags(self, tags):
        """タグリストを更新する.

        :param List[str] tags: タグリスト
        """
        self._tags = ','.join(sorted(set(self.to_tags_list(tags))))

    @classmethod
    def to_tags_list(cls, tags):
        """タグリストをリスト形式に変換する.

        :param Union[str, List[str], Tuple[str]] tags: 変換前タグリスト
        :return: 変換後タグリスト
        :rtype: Union[List, Tuple]
        """
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
    def attributes(self):
        """属性リストを返す.

        :return: 属性リスト
        :rtype: ModuleAttributes
        """
        return ModuleAttributes(self._attributes)

    @attributes.setter  # type: ignore
    def attributes(self, attributes):
        """属性リストを更新する.

        :param Union[ModuleAttributes, str, Tuple, List] attributes: 属性リスト
        """
        if not isinstance(attributes, ModuleAttributes):
            attributes = ModuleAttributes(attributes)
        self._attributes = str(attributes)

    def to_json(self, with_boxes=False, with_schema=False, with_cc_info=False):
        """このモデルのJSON表現を返す.

        :param bool with_boxes: 返り値にMessageBoxの情報を含めるか
        :param bool with_schema: 返り値にSchemaの情報を含めるか
        :param bool with_cc_info: 返り値にowner CircleCoreの情報を含めるか
        :return: JSON表現のDict
        :rtype: Dict
        """
        d = {
            'uuid': str(self.uuid),
            'ccUuid': str(self.cc_uuid),
            'messageBoxUuids': [str(box.uuid) for box in self.message_boxes],
            'displayName': self.display_name,
            'tags': [tag for tag in self.tags],
            'attributes': [prop.to_json() for prop in self.attributes],
            'memo': self.memo,
        }

        if with_boxes:
            d['messageBoxes'] = [box.to_json(with_schema=with_schema, with_slave_cc_infos=with_cc_info)
                                 for box in self.message_boxes]

        if with_cc_info:
            d['ccInfo'] = self.cc_info.to_json()
            d['isReplication'] = self.cc_info.myself is False

        return d

    def update_from_json(self, jsonobj, with_boxes=False):
        """JSON表現からモデルを更新する.

        :param Dict jsonobj: JSON表現のDict
        :param bool with_boxes: MessageBoxも更新するか.
        """
        self.display_name = jsonobj.get('displayName', self.display_name)
        self.tags = jsonobj.get('tags', self.tags)
        if 'attributes' in jsonobj:
            self.attributes = ModuleAttributes(jsonobj['attributes'])
        self.memo = jsonobj.get('memo', self.memo)

        if with_boxes and 'messageBoxes' in jsonobj:
            if self.cc_info and self.cc_info.myself is False:
                raise ValueError('cannot update box of replication module')

            boxes = []
            # TODO: in queryとか使う
            for box_data in jsonobj['messageBoxes']:
                box_uuid = box_data.get('uuid')
                if not box_uuid:
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
            self.message_boxes = boxes
