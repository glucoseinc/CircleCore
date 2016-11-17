#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Device Model."""

# community module
from six import PY3


if PY3:
    from typing import Dict


class Device(object):
    """Deviceオブジェクト.

    :param str schema_uuid: Schema UUID
    :param str display_name: 表示名
    :param properties: プロパティ
    :type properties: Dict[str, str]
    """

    def __init__(self, schema, display_name, **kwargs):
        """init.

        :param str schema: Schema UUID
        :param str display_name: 表示名
        """
        self.schema_uuid = schema
        self.display_name = display_name
        self.properties = {}
        property_keys = [k for k in kwargs.keys() if k.startswith('property')]
        for property_key in property_keys:
            idx = property_key[8:]
            property_type = 'value' + idx
            if property_type in kwargs.keys():
                self.properties[kwargs[property_key]] = kwargs[property_type]
