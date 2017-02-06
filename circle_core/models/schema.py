# -*- coding: utf-8 -*-

"""Schema Model."""

# system module
import collections
import datetime

# community module
import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy.ext.hybrid import hybrid_property

# project module
from .base import GUID, MetaDataBase


class SchemaProperty(collections.namedtuple('SchemaProperty', ['name', 'type'])):
    def __new__(cls, name, type=None):
        if isinstance(name, dict):
            name, type = name['name'], name['type']
        if type is None and ':' in name:
            name, type = name.split(':', 2)
        if type is None or ':' in type or ':' in name:
            raise ValueError('invalid property')

        return super(SchemaProperty, cls).__new__(cls, name, type.lower())

    def __str__(self):
        return '{}:{}'.format(self.name, self.type)


class SchemaProperties(object):
    def __init__(self, props):
        self._properties = []

        if isinstance(props, str):
            props = props.split(',')
        if isinstance(props, (tuple, list)):
            for p in props:
                self.append(p)

    def __iter__(self):
        return iter(self._properties)

    def __len__(self):
        return len(self._properties)

    def __str__(self):
        return ','.join(str(p) for p in self)

    def append(self, p):
        if not isinstance(p, SchemaProperty):
            p = SchemaProperty(p)
        return self._properties.append(p)


class Schema(MetaDataBase):
    """Schemaオブジェクト.

    :param UUID uuid: Schema UUID
    :param str display_name: 表示名
    :param List[SchemaProperty] properties: プロパティ
    :param Optional[str] memo: メモ
    """
    __tablename__ = 'schemas'

    uuid = sa.Column(GUID, primary_key=True)
    display_name = sa.Column(sa.String(255), nullable=False, default='')
    _properties = sa.Column('properties', sa.Text, nullable=False, default='')
    memo = sa.Column(sa.Text, nullable=False, default='')
    created_at = sa.Column(sa.DateTime, nullable=False, default=datetime.datetime.utcnow)
    updated_at = sa.Column(
        sa.DateTime, nullable=False,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow)

    message_boxes = orm.relationship('MessageBox', backref='schema')

    def __init__(self, uuid, display_name, properties=None, **kwargs):
        """init.

        :param Union[str, UUID] uuid: Schema UUID
        :param str display_name: 表示名
        :param Optional[List[Dict[str, str]]] dictified_properties: 辞書化プロパティ
        :param Optional[str] memo: メモ
        """

        if not isinstance(properties, SchemaProperties):
            properties = SchemaProperties(properties)

        super(Schema, self).__init__(uuid=uuid, display_name=display_name, _properties=str(properties), **kwargs)

    def __eq__(self, other):
        """return equality.

        :param Schema other: other Schema
        :return: equality
        :rtype: bool
        """
        return all([self.uuid == other.uuid, self.display_name == other.display_name,
                    self.properties == other.properties,
                    self.memo == other.memo])

    @hybrid_property
    def properties(self):
        return SchemaProperties(self._properties)

    @properties.setter
    def properties(self, properties):
        if not isinstance(properties, SchemaProperties):
            properties = SchemaProperties(properties)
        self._properties = str(properties)

    # @property
    # def stringified_properties(self):
    #     """プロパティを文字列化する.

    #     :return: 文字列化プロパティ
    #     :rtype: str
    #     """
    #     strings = []
    #     for prop in self.properties:
    #         strings.append('{}:{}'.format(prop.name, prop.type))
    #     return ','.join(strings)

    # @property
    # def dictified_properties(self):
    #     """プロパティを辞書化する.

    #     :return: 辞書化プロパティ
    #     :rtype: List[Dict[str, str]]
    #     """
    #     return [prop.to_json() for prop in self.properties]

    # @classmethod
    # def dictify_properties(cls, stringified_properties):
    #     """文字列化プロパティを辞書化する.

    #     :param str stringified_properties: 文字列化プロパティ
    #     :return: 辞書化プロパティ
    #     :rtype: List[Dict[str, str]]
    #     """
    #     dictified_properties = []
    #     property_strings = stringified_properties.split(',')
    #     for property_string in property_strings:
    #         _name, _type = property_string.split(':')
    #         dictified_properties.append({
    #             'name': _name,
    #             'type': _type,
    #         })
    #     return dictified_properties

    # def to_json(self):
    #     """このモデルのJSON表現を返す.

    #     :return: json表現のdict
    #     :rtype: Dict
    #     """
    #     return {
    #         'uuid': str(self.uuid),
    #         'displayName': self.display_name,
    #         'properties': self.dictified_properties,
    #         'memo': self.memo,
    #     }

    # @classmethod
    # def from_json(cls, json_msg, **kwargs):
    #     """JSON表現から復元.

    #     :param dict json_msg:
    #     :rtype: Schema
    #     """
    #     properties = json_msg.pop('properties')
    #     return Schema(dictified_properties=properties, **json_msg, **kwargs)

    # @property
    # def master_uuid(self):
    #     """
    #     :rtype Optional[UUID]:
    #     """
    #     for box in metadata().message_boxes:
    #         if box.schema_uuid == self.uuid and box.master_uuid:
    #             return box.master_uuid

    #     return None

    def check_match(self, data):  # TODO: Schema専用のJSONDecoderを作ってそこで例外を投げたほうがいいかなあ
        """nanomsg経由で受け取ったメッセージをデシリアライズしたものがこのSchemaに適合しているか.
        :param dict dic:
        """
        if not len(data) == len(self.properties):
            return False

        schema_type_map = {
            'float': float,
            'int': int,
            'text': str
        }

        for msg_key, msg_value in data.items():
            for property in self.properties:
                if msg_key == property.name and (
                    (property.type == 'float' and isinstance(msg_value, int)) or
                    # float型の値が0だった場合にintだと判定されてしまう
                    isinstance(msg_value, schema_type_map[property.type])
                ):
                    break
            else:
                return False

        return True
