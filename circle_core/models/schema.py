#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Schema(object):
    def __init__(self, uuid, display_name, **kwargs):
        self.uuid = uuid
        self.display_name = display_name
        self.properties = {}
        property_keys = [k for k in kwargs.keys() if k.startswith('key')]
        for property_key in property_keys:
            idx = property_key[3:]
            property_type = 'type' + idx
            if property_type in kwargs.keys():
                self.properties[kwargs[property_key]] = kwargs[property_type]

    # TODO: 整形して返す
    def __str__(self):
        return 'schema_string'
