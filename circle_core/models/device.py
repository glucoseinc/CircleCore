#!/usr/bin/env python
# -*- coding: utf-8 -*-

from six import PY3


if PY3:
    from typing import Dict  # noqa


class Device(object):
    def __init__(self, schema, display_name, **kwargs):
        self.schema_uuid = schema
        self.display_name = display_name
        self.properties = {}  # type: Dict[str, str]
        property_keys = [k for k in kwargs.keys() if k.startswith('property')]
        for property_key in property_keys:
            idx = property_key[8:]
            property_type = 'value' + idx
            if property_type in kwargs.keys():
                self.properties[kwargs[property_key]] = kwargs[property_type]

    # TODO: 整形して返す
    def __str__(self):
        return 'device_string'
