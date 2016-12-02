# -*- coding: utf-8 -*-

"""Device Model."""

# system module
import re
from uuid import UUID

# community module
from six import PY3

if PY3:
    from typing import List, Optional, Tuple, Union


class DeviceProperty(object):
    """DevicePropertyオブジェクト.

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


class Device(object):
    """Deviceオブジェクト.

    :param UUID uuid: Device UUID
    :param Optional[str] display_name: 表示名
    :param str schema_uuid: Schema UUID
    :param List[DeviceProperty] properties: プロパティ
    """

    def __init__(self, uuid, schema_uuid, display_name=None, **kwargs):
        """init.

        :param Union[str, UUID] uuid; Device UUID
        :param Union[str, UUID] schema_uuid: Schema UUID
        :param Optional[str] display_name: 表示名
        """
        if not isinstance(uuid, UUID):
            uuid = UUID(uuid)
        if not isinstance(schema_uuid, UUID):
            schema_uuid = UUID(schema_uuid)

        self.uuid = uuid
        self.schema_uuid = schema_uuid
        self.display_name = display_name
        self.properties = []
        property_names = sorted([k for k in kwargs.keys() if k.startswith('property')])
        for property_name in property_names:
            idx = property_name[8:]
            property_value = 'value' + idx
            if property_value in kwargs.keys():
                self.properties.append(DeviceProperty(kwargs[property_name], kwargs[property_value]))

    @property
    def stringified_properties(self):
        """プロパティを文字列化する.

        :return: 文字列化プロパティ
        :rtype: str
        """
        strings = []
        for prop in self.properties:
            strings.append('{}:{}'.format(prop.name, prop.value))
        return ', '.join(strings)

    @property
    def storage_key(self):
        """ストレージキー.

        :return: ストレージキー
        :rtype: str
        """
        return 'device_{}'.format(self.uuid)

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
                self.properties.append(DeviceProperty(name, value))

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
        pattern = r'^device_[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$'
        return re.match(pattern, key) is not None
