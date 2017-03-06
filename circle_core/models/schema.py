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
from .base import generate_uuid, GUID, UUIDMetaDataBase
from ..constants import CRDataType


# type annotation
try:
    from typing import Dict, List, Optional, Union, Tuple, TYPE_CHECKING
    if TYPE_CHECKING:
        from uuid import UUID
        from .message_box import MessageBox
except ImportError:
    pass


class SchemaProperty(collections.namedtuple('SchemaProperty', ['name', 'type'])):
    """SchemaProperty."""

    def __new__(cls, name, type=None):
        """new.

        :param Union[Dict, str] name: プロパティ名またはプロパティ名とプロパティタイプ
        :param Optional[str] type: プロパティタイプ
        """
        if isinstance(name, dict):
            name, type = name['name'], name['type']
        if type is None and ':' in name:
            name, type = name.split(':', 2)
        if type is None or ':' in type or ':' in name:
            raise ValueError('invalid property')

        return super(SchemaProperty, cls).__new__(cls, name, type.lower())

    def __str__(self):
        """str.

        :return: 文字列表現
        :rtype: str
        """
        return '{}:{}'.format(self.name, self.type)

    def to_json(self):
        """このモデルのJSON表現を返す.

        :return: JSON表現のDict
        :rtype: Dict
        """
        return {
            'name': self.name,
            'type': self.type
        }


class SchemaProperties(object):
    """SchemaProperties.

    :param List[SchemaProperty] _properties: SchemaPropertyリスト
    """

    def __init__(self, props):
        """init.

        :param Union[str, Tuple, List] props: プロパティ名とプロパティタイプ
        """
        self._properties = []

        if isinstance(props, str):
            props = props.split(',')
        if isinstance(props, (tuple, list)):
            for p in props:
                self.append(p)

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
        return ','.join(str(p) for p in self)

    def append(self, p):
        """SchemaPropertyを追加する.

        :param Union[SchemaProperty] p: SchemaProperty
        :return: None
        :rtype: None
        """
        if not isinstance(p, SchemaProperty):
            p = SchemaProperty(p)
        return self._properties.append(p)


class Schema(UUIDMetaDataBase):
    """Schemaオブジェクト.

    :param UUID uuid: Schema UUID
    :param str display_name: 表示名
    :param str _properties: プロパティ
    :param List[SchemaProperty] properties: プロパティ
    :param str memo: メモ
    :param datetime.datetime created_at: 作成日時
    :param datetime.datetime updated_at: 更新日時
    :param List[MessageBox] message_boxes: MessageBox
    """

    __tablename__ = 'schemas'

    uuid = sa.Column(GUID, primary_key=True)
    cc_uuid = sa.Column(GUID, sa.ForeignKey('cc_informations.uuid', name='fk_schemas_cc_uuid'), nullable=False)
    display_name = sa.Column(sa.String(255), nullable=False, default='')
    _properties = sa.Column('properties', sa.Text, nullable=False, default='')
    memo = sa.Column(sa.Text, nullable=False, default='')
    created_at = sa.Column(sa.DateTime, nullable=False, default=datetime.datetime.utcnow)
    updated_at = sa.Column(sa.DateTime, nullable=False, default=datetime.datetime.utcnow,
                           onupdate=datetime.datetime.utcnow)

    message_boxes = orm.relationship('MessageBox', backref='schema')

    @classmethod
    def create(cls, **kwargs):
        """このモデルを作成する.

        :param Dict kwargs: キーワード引数
        :return: Schemaオブジェクト
        :rtype: Schema
        """
        if 'cc_uuid' not in kwargs:
            from .cc_info import CcInfo
            kwargs['cc_uuid'] = CcInfo.query.filter_by(myself=True).one().uuid

        schema = cls(
            uuid=generate_uuid(model=cls),
            **kwargs
        )
        return schema

    def __init__(self, **kwargs):
        """init.

        :param Dict kwargs: キーワード引数
        """

        if 'properties' in kwargs:
            properties = kwargs['properties']
            if not isinstance(properties, SchemaProperties):
                kwargs['properties'] = SchemaProperties(properties)

        super(Schema, self).__init__(**kwargs)

    def __hash__(self):
        """hash.

        :return: ハッシュ値
        :rtype: int
        """
        return hash('{}:{!r}'.format(self.__class__.__name__, hash(self.uuid)))

    def __eq__(self, other):
        """eq.

        :param Schema other: other Schema
        :return: equality
        :rtype: bool
        """
        return all([self.uuid == other.uuid, self.display_name == other.display_name,
                    self.properties == other.properties,
                    self.memo == other.memo])

    @hybrid_property
    def properties(self):
        """プロパティリストを返す.

        :return: プロパティリスト
        :rtype: SchemaProperties
        """
        return SchemaProperties(self._properties)

    @properties.setter
    def properties(self, properties):
        """プロパティリストを更新する.

        :param Union[SchemaProperties, str, Tuple, List] properties: プロパティリスト
        """
        if not isinstance(properties, SchemaProperties):
            properties = SchemaProperties(properties)
        self._properties = str(properties)

    def to_json(self, with_modules=False):
        """このモデルのJSON表現を返す.

        :param bool with_modules: 返り値にModuleの情報を含めるか
        :return: JSON表現のDict
        :rtype: Dict
        """
        d = {
            'uuid': str(self.uuid),
            'ccUuid': str(self.cc_uuid),
            'displayName': self.display_name,
            'properties': [prop.to_json() for prop in self.properties],
            'memo': self.memo,
        }

        if with_modules:
            modules = {}
            for box in self.message_boxes:
                modules[box.module.uuid] = box.module
            d['modules'] = [module.to_json() for module in modules.values()]

        return d

    def update_from_json(self, jsonobj):
        """JSON表現からモデルを更新する.

        :param Dict jsonobj: JSON表現のDict
        """
        self.display_name = jsonobj.get('displayName', self.display_name)
        self.memo = jsonobj.get('memo', self.memo)
        if 'properties' in jsonobj:
            self.properties = SchemaProperties(jsonobj['properties'])

    def check_match(self, data):
        """nanomsg経由で受け取ったメッセージをデシリアライズしたものがこのSchemaに適合しているか.

        :param Dict data:
        :return: 適合可否
        :rtype: bool
        """
        # TODO: Schema専用のJSONDecoderを作ってそこで例外を投げる
        if not len(data) == len(self.properties):
            return False

        # TODO: 各Typeをクラス化する
        # TODO: もう少し厳密にvalidate
        def validate_int(value):
            return isinstance(value, int)

        def validate_float(value):
            return isinstance(value, (int, float))

        def validate_bool(value):
            return isinstance(value, bool)

        def validate_string(value):
            return isinstance(value, str)

        def validate_bytes(value):
            return isinstance(value, str)

        def validate_date(value):
            return isinstance(value, str)

        def validate_datetime(value):
            return isinstance(value, str)

        def validate_time(value):
            return isinstance(value, str)

        def validate_timestamp(value):
            return isinstance(value, str)

        validator = {
            CRDataType.INT.value: validate_int,
            CRDataType.FLOAT.value: validate_float,
            CRDataType.BOOL.value: validate_bool,
            CRDataType.STRING.value: validate_string,
            CRDataType.BYTES.value: validate_bytes,
            CRDataType.DATE.value: validate_date,
            CRDataType.DATETIME.value: validate_datetime,
            CRDataType.TIME.value: validate_time,
            CRDataType.TIMESTAMP.value: validate_timestamp,
        }

        for msg_key, msg_value in data.items():
            for prop in self.properties:
                if msg_key == prop.name and validator[prop.type.upper()](msg_value):
                    break
            else:
                return False

        return True
