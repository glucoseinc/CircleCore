# -*- coding: utf-8 -*-
"""Schema Model."""

# system module
import collections
import datetime
from typing import Any, Dict, List, Optional, TYPE_CHECKING, Tuple, Union, cast

# community module
import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy.ext.hybrid import hybrid_property

# project module
from .base import GUID, UUIDMetaDataBase, generate_uuid
from ..constants import CRDataType
from ..types import BlobMetadata

# type annotation
if TYPE_CHECKING:
    from uuid import UUID

    from mypy_extensions import TypedDict

    class SchemaPropertyJson(TypedDict, total=True):
        name: str
        type: str

    class SchemaJson(TypedDict, total=False):
        uuid: str
        ccUuid: str
        displayName: str
        properties: List[SchemaPropertyJson]
        memo: str
        # modules: List[ModuleJson]
        modules: List[Dict[str, Any]]

    from .message_box import MessageBox


class SchemaProperty(collections.namedtuple('SchemaProperty', ['name', 'raw_type'])):
    """SchemaProperty."""
    name: str
    raw_type: str

    def __new__(cls, name: 'Union[SchemaPropertyJson, str]', type: Optional[str] = None):
        """new.

        Args:
            name: プロパティ名またはプロパティ名とプロパティタイプ
            type: プロパティタイプ
        """
        if isinstance(name, dict):
            name, type = name['name'], name['type']
        if type is None and ':' in name:
            name, type = cast(str, name).split(':', 2)
        if type is None or ':' in type or ':' in name:
            raise ValueError('invalid property')

        return super(SchemaProperty, cls).__new__(cls, name, type.lower())

    def __str__(self):
        """str.

        :return: 文字列表現
        :rtype: str
        """
        return '{}:{}'.format(self.name, self.raw_type)

    def to_json(self) -> 'SchemaPropertyJson':
        """このモデルのJSON表現を返す.

        :return: JSON表現のDict
        :rtype: Dict
        """
        return {'name': self.name, 'type': self.raw_type}

    @property
    def type(self) -> Optional[str]:
        # Deprecatedにしたい
        return self.raw_type

    @property
    def type_val(self) -> Optional[CRDataType]:
        return CRDataType[self.raw_type.upper()] if self.raw_type else None


class SchemaProperties(object):
    """SchemaProperties.

    Attributes:
        _properties: SchemaPropertyリスト

    Args:
        props: プロパティ名とプロパティタイプ
    """
    _properties: List[SchemaProperty]

    def __init__(self, props: Union[str, Tuple[str, ...], List[str]]):
        """init.
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

    def __len__(self) -> int:
        """len.

        Returns:
            int: 長さ
        """
        return len(self._properties)

    def __str__(self) -> str:
        """str.

        Returns:
            str: 文字列表現
        """
        return ','.join(str(p) for p in self)

    def append(self, p: 'Union[SchemaProperty]') -> None:
        """SchemaPropertyを追加する.

        Args:
            p (Union[SchemaProperty]): SchemaProperty
        """
        if not isinstance(p, SchemaProperty):
            p = SchemaProperty(p)
        self._properties.append(p)


class Schema(UUIDMetaDataBase):
    """Schemaオブジェクト.

    Attributes:
        message_boxes List[circle_core.models.MessageBox]: MessageBox
        uuid: Schema UUID
        display_name (str): 表示名
        _properties (str): プロパティ
        properties (List[circle_core.models.SchemaProperties]): プロパティ
        memo (str): メモ
        created_at (datetime.datetime): 作成日時
        updated_at (datetime.datetime): 更新日時

    Args:
        kwargs (Dict): キーワード引数
    """
    message_boxes: 'List[MessageBox]'
    uuid: 'UUID'

    __tablename__ = 'schemas'

    uuid = sa.Column(GUID, primary_key=True)
    cc_uuid = sa.Column(GUID, sa.ForeignKey('cc_informations.uuid', name='fk_schemas_cc_uuid'), nullable=False)
    display_name = sa.Column(sa.String(255), nullable=False, default='')
    _properties = sa.Column('properties', sa.Text, nullable=False, default='')
    memo = sa.Column(sa.Text, nullable=False, default='')
    created_at = sa.Column(sa.DateTime, nullable=False, default=datetime.datetime.utcnow)
    updated_at = sa.Column(
        sa.DateTime, nullable=False, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow
    )

    message_boxes = orm.relationship('MessageBox', backref='schema')

    @classmethod
    def create(cls, **kwargs) -> 'Schema':
        """このモデルを作成する.

        Args:
            kwargs (Dict): キーワード引数

        Returns:
            circle_core.models.Schema: Schemaオブジェクト
        """
        if 'cc_uuid' not in kwargs:
            from .cc_info import CcInfo
            kwargs['cc_uuid'] = CcInfo.query.filter_by(myself=True).one().uuid

        schema = cls(uuid=generate_uuid(model=cls), **kwargs)
        return schema

    def __init__(self, **kwargs):
        """init.
        """

        if 'properties' in kwargs:
            properties = kwargs['properties']
            if not isinstance(properties, SchemaProperties):
                kwargs['properties'] = SchemaProperties(properties)

        super(Schema, self).__init__(**kwargs)

    def __hash__(self):
        """hash.

        Returns:
            int: ハッシュ値
        """
        return hash('{}:{!r}'.format(self.__class__.__name__, hash(self.uuid)))

    def __eq__(self, other):
        """eq.

        Args:
            other (Schema): other Schema

        Returns:
            bool: equality
        """
        return all(
            [
                self.uuid == other.uuid, self.display_name == other.display_name, self.properties == other.properties,
                self.memo == other.memo
            ]
        )

    @hybrid_property
    def properties(self):
        """プロパティリストを返す.

        Returns:
            circle_core.models.SchemaProperties: プロパティリスト
        """
        return SchemaProperties(self._properties)

    @properties.setter  # type: ignore
    def properties(self, properties):
        """プロパティリストを更新する.

        Args:
            properties (Union[circle_core.models.SchemaProperties, str, Tuple, List]): プロパティリスト
        """
        if not isinstance(properties, SchemaProperties):
            properties = SchemaProperties(properties)
        self._properties = str(properties)

    def to_json(self, with_modules=False) -> 'SchemaJson':
        """このモデルのJSON表現を返す.

        Args:
            with_modules (bool): 返り値にModuleの情報を含めるか

        Returns:
            SchemaJson: JSON表現のDict
        """
        d: 'SchemaJson' = {
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
            d['modules'] = [module.to_json() for module in modules.values()]  # type: ignore

        return d

    def update_from_json(self, jsonobj):
        """JSON表現からモデルを更新する.

            jsonobj (Dict): JSON表現のDict
        """
        self.display_name = jsonobj.get('displayName', self.display_name)
        self.memo = jsonobj.get('memo', self.memo)
        if 'properties' in jsonobj:
            self.properties = SchemaProperties(jsonobj['properties'])

    def check_match(self, data) -> 'Tuple[bool, Optional[str]]':
        """nanomsg経由で受け取ったメッセージをデシリアライズしたものがこのSchemaに適合しているか.

        Args:
            data (Dict):

        Returns:
            bool: 適合可否
        """
        # TODO: Schema専用のJSONDecoderを作ってそこで例外を投げる
        if not len(data) == len(self.properties):
            return False, 'size mismatch'

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

        def validate_blob(value):
            return isinstance(value, BlobMetadata)

        validator = {
            CRDataType.INT: validate_int,
            CRDataType.FLOAT: validate_float,
            CRDataType.BOOL: validate_bool,
            CRDataType.STRING: validate_string,
            CRDataType.BYTES: validate_bytes,
            CRDataType.DATE: validate_date,
            CRDataType.DATETIME: validate_datetime,
            CRDataType.TIME: validate_time,
            CRDataType.TIMESTAMP: validate_timestamp,
            CRDataType.BLOB: validate_blob,
        }

        for msg_key, msg_value in data.items():
            if msg_value is None:
                continue
            for prop in self.properties:
                if msg_key == prop.name and validator[prop.type_val](msg_value):
                    break
            else:
                return False, '`{}` validation failed'.format(msg_key)

        return True, None
