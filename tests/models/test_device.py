#!/usr/bin/env python
# -*- coding: utf-8 -*-

from circle_core.models.device import Device
import pytest


class TestDevice(object):
    @pytest.mark.parametrize(('schema', 'display_name', 'kwargs', 'expected'), [
        ('UUID', 'DISP_NAME', {'property1': 'hoge', 'value1': 'int'},
         {'schema': 'UUID', 'display_name': 'DISP_NAME', 'properties': {'hoge': 'int'}}),
    ])
    def test_init(self, schema, display_name, kwargs, expected):
        device = Device(schema, display_name, **kwargs)
        assert device.schema_uuid == expected['schema']
        assert device.display_name == expected['display_name']
        for k, v in device.properties.items():
            assert k in expected['properties']
            assert v == expected['properties'][k]
