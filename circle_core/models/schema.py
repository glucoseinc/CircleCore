# -*- coding: utf-8 -*-

"""Schema Model."""

# community module
from six import PY3

if PY3:
    from typing import List, Optional


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


class Schema(object):
    """Schemaオブジェクト.

    :param str uuid: Schema UUID
    :param Optional[str] display_name: 表示名
    :param List[SchemaProperty] properties: プロパティ
    """

    def __init__(self, uuid, display_name=None, **kwargs):
        """init.

        :param str uuid: Schema UUID
        :param Optional[str] display_name: 表示名
        """
        self.uuid = uuid
        self.display_name = display_name
        self.properties = []
        property_names = sorted([k for k in kwargs.keys() if k.startswith('key')])
        for property_name in property_names:
            idx = property_name[3:]
            property_type = 'type' + idx
            if property_type in kwargs.keys():
                self.properties.append(SchemaProperty(kwargs[property_name], kwargs[property_type]))

    @property
    def stringified_properties(self):
        """プロパティを文字列化する.

        :return: 文字列化プロパティ
        :rtype: str
        """
        strings = []
        for prop in self.properties:
            strings.append('{}:{}'.format(prop.name, prop.type))
        return ', '.join(strings)
