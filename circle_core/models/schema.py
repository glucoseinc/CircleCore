#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Schema Model."""

# community module
from six import PY3


if PY3:
    from typing import Dict


class Schema(object):
    """Schemaオブジェクト.

    :param str uuid: Schema UUID
    :param str display_name: 表示名
    :param properties: プロパティ
    :type properties: Dict[str, str]
    """

    def __init__(self, uuid, display_name, **kwargs):
        """init.

        :param str uuid: Schema UUID
        :param str display_name: 表示名
        """
        self.uuid = uuid
        self.display_name = display_name
        self.properties = {}
        property_keys = [k for k in kwargs.keys() if k.startswith('key')]
        for property_key in property_keys:
            idx = property_key[3:]
            property_type = 'type' + idx
            if property_type in kwargs.keys():
                self.properties[kwargs[property_key]] = kwargs[property_type]
