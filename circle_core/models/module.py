# -*- coding: utf-8 -*-

"""Module Model."""

# system module
import re
from uuid import UUID

# community module
from six import PY3

if PY3:
    from typing import List, Optional, Tuple, Union


class ModuleProperty(object):
    """ModulePropertyオブジェクト.

    :param str name: 属性名
    :param str value: 属性値
    """

    def __init__(self, name, value):
        """init.

        :param str name: 属性名
        :param str value: 属性値
        """
        self.name = name
        self.value = value


class Module(object):
    """Moduleオブジェクト.

    :param UUID uuid: Module UUID
    :param Optional[str] display_name: 表示名
    :param str schema_uuid: Schema UUID
    :param List[ModuleProperty] properties: プロパティ
    """

    def __init__(self, uuid, schema_uuid, display_name=None, properties=None):
        """init.

        :param Union[str, UUID] uuid; Module UUID
        :param Union[str, UUID] schema_uuid: Schema UUID
        :param Optional[str] display_name: 表示名
        :param Optional[str] properties: プロパティ
        """
        if not isinstance(uuid, UUID):
            uuid = UUID(uuid)
        if not isinstance(schema_uuid, UUID):
            schema_uuid = UUID(schema_uuid)

        self.uuid = uuid
        self.schema_uuid = schema_uuid
        self.display_name = display_name
        self.properties = []
        if properties is not None:
            name_and_values = properties.split(',')
            for name_and_value in name_and_values:
                _name, _value = name_and_value.split(':', 1)
                self.properties.append(ModuleProperty(_name, _value))

    @property
    def stringified_properties(self):
        """プロパティを文字列化する.

        :return: 文字列化プロパティ
        :rtype: str
        """
        strings = []
        for prop in self.properties:
            strings.append('{}:{}'.format(prop.name, prop.value))
        return ','.join(strings)

    @property
    def storage_key(self):
        """ストレージキー.

        :return: ストレージキー
        :rtype: str
        """
        return 'module_{}'.format(self.uuid)

    def append_properties(self, name_and_values):
        """プロパティを追加する.

        :param List[Tuple[str, str]] name_and_values: 属性名と属性値のタプルのリスト
        """
        for name, value in name_and_values:
            for prop in self.properties:
                if prop.name == name:
                    prop.value = value
                    break
            else:
                self.properties.append(ModuleProperty(name, value))

    def remove_properties(self, names):
        """プロパティを除去する.

        :param List[str] names: 属性名リスト
        """
        self.properties = [prop for prop in self.properties if prop.name not in names]

    @classmethod
    def is_key_matched(cls, key):
        """指定のキーがストレージキーの形式にマッチしているか.

        :param str key:
        :return: マッチしているか
        :rtype: bool
        """
        pattern = r'^module_[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$'
        return re.match(pattern, key) is not None
