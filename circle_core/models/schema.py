# -*- coding: utf-8 -*-

"""Schema Model."""

# system module
from uuid import UUID

# community module
from six import PY3

# project module
from .base import UUIDBasedObject
from ..helpers.metadata import metadata

if PY3:
    from typing import Dict, List, Optional, Union


class SchemaError(Exception):
    pass


class SchemaProperty(object):
    """SchemaPropertyオブジェクト.

    :param str name: 属性名
    :param str type: タイプ
    """

    def __init__(self, name, property_type):
        """init.

        :param str name: キー
        :param str property_type: タイプ
        """
        self.name = name
        self.type = property_type

    def __eq__(self, other):
        """return equality.

        :param SchemaProperty other: other SchemaProperty
        :return: equality
        :rtype: bool
        """
        return all([self.name == other.name, self.type == other.type])

    def to_json(self):
        """このモデルのJSON表現を返す.

        :return: json表現のdict
        :rtype: Dict
        """
        return {
            'name': self.name,
            'type': self.type,
        }


class Schema(UUIDBasedObject):
    """Schemaオブジェクト.

    :param str key_prefix: ストレージキーのプレフィックス
    :param UUID uuid: Schema UUID
    :param str display_name: 表示名
    :param List[SchemaProperty] properties: プロパティ
    :param Optional[str] memo: メモ
    """

    key_prefix = 'schema'

    def __init__(self, uuid, display_name, dictified_properties=None, memo=None):
        """init.

        :param Union[str, UUID] uuid: Schema UUID
        :param str display_name: 表示名
        :param Optional[List[Dict[str, str]]] dictified_properties: 辞書化プロパティ
        :param Optional[str] memo: メモ
        """
        super(Schema, self).__init__(uuid)

        self.display_name = display_name
        self.properties = []
        if dictified_properties is not None:
            for dictified_property in dictified_properties:
                _name, _type = dictified_property.get('name'), dictified_property.get('type')
                if _name is not None and _type is not None:
                    self.properties.append(SchemaProperty(_name.strip(), _type.strip()))
        self.memo = memo

    def __eq__(self, other):
        """return equality.

        :param Schema other: other Schema
        :return: equality
        :rtype: bool
        """
        return all([self.uuid == other.uuid, self.display_name == other.display_name,
                    self.properties == other.properties,
                    self.memo == other.memo])

    @property
    def stringified_properties(self):
        """プロパティを文字列化する.

        :return: 文字列化プロパティ
        :rtype: str
        """
        strings = []
        for prop in self.properties:
            strings.append('{}:{}'.format(prop.name, prop.type))
        return ','.join(strings)

    @property
    def dictified_properties(self):
        """プロパティを辞書化する.

        :return: 辞書化プロパティ
        :rtype: List[Dict[str, str]]
        """
        return [prop.to_json() for prop in self.properties]

    @classmethod
    def dictify_properties(cls, stringified_properties):
        """文字列化プロパティを辞書化する.

        :param str stringified_properties: 文字列化プロパティ
        :return: 辞書化プロパティ
        :rtype: List[Dict[str, str]]
        """
        dictified_properties = []
        property_strings = stringified_properties.split(',')
        for property_string in property_strings:
            _name, _type = property_string.split(':')
            dictified_properties.append({
                'name': _name,
                'type': _type,
            })
        return dictified_properties

    def to_json(self):
        """このモデルのJSON表現を返す.

        :return: json表現のdict
        :rtype: Dict
        """
        return {
            'uuid': str(self.uuid),
            'display_name': self.display_name,
            'properties': self.dictified_properties,
            'memo': self.memo,
        }

    @classmethod
    def from_json(cls, json_msg, **kwargs):
        """JSON表現から復元.

        :param dict json_msg:
        :rtype: Schema
        """
        properties = json_msg.pop('properties')
        return Schema(dictified_properties=properties, **json_msg, **kwargs)

    @property
    def master_uuid(self):
        """
        :rtype Optional[UUID]:
        """
        for box in metadata().message_boxes:
            if box.schema_uuid == self.uuid and box.master_uuid:
                return box.master_uuid

        return None

    def is_valid(self, dic):  # TODO: Schema専用のJSONDecoderを作ってそこで例外を投げたほうがいいかなあ
        """nanomsg経由で受け取ったメッセージをデシリアライズしたものがこのSchemaに適合しているか.
        :param dict dic:
        """
        if not len(dic) == len(self.properties):
            return False

        schema_type_map = {
            'float': float,
            'int': int,
            'text': str
        }

        for msg_key, msg_value in dic.items():
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
