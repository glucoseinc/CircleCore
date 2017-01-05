# -*- coding: utf-8 -*-

"""Schema Model."""

# system module
import re
from uuid import UUID

# community module
from six import PY3

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

    @property
    def dictified(self):
        return {
            'name': self.name,
            'type': self.type,
        }


class Schema(object):
    """Schemaオブジェクト.

    :param UUID uuid: Schema UUID
    :param Optional[str] display_name: 表示名
    :param List[SchemaProperty] properties: プロパティ
    :param Optional[str] memo: メモ
    """

    def __init__(self, uuid, display_name=None, dictified_properties=None, memo=None):
        """init.

        :param Union[str, UUID] uuid: Schema UUID
        :param Optional[str] display_name: 表示名
        :param Optional[List[Dict[str, str]]] dictified_properties: 辞書化プロパティ
        :param Optional[str] memo: メモ
        """
        if not isinstance(uuid, UUID):
            try:
                uuid = UUID(uuid)
            except ValueError:
                raise SchemaError('Invalid uuid : {}'.format(uuid))

        self.uuid = uuid
        self.display_name = display_name
        self.properties = []
        if dictified_properties is not None:
            for dictified_property in dictified_properties:
                _name, _type = dictified_property.get('name'), dictified_property.get('type')
                if _name is not None and _type is not None:
                    self.properties.append(SchemaProperty(_name.strip(), _type.strip()))
        self.memo = memo

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
        return [prop.dictified for prop in self.properties]

    @property
    def storage_key(self):
        """ストレージキー.

        :return: ストレージキー
        :rtype: str
        """
        return 'schema_{}'.format(self.uuid)

    @classmethod
    def is_key_matched(cls, key):
        """指定のキーがストレージキーの形式にマッチしているか.

        :param str key:
        :return: マッチしているか
        :rtype: bool
        """
        pattern = r'^schema_[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$'
        return re.match(pattern, key) is not None

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
