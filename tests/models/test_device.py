# -*- coding: utf-8 -*-

from circle_core.models.device import Device
import pytest


class TestDevice(object):
    @pytest.mark.parametrize(('device_uuid', 'schema_uuid', 'display_name', 'kwargs', 'expected'), [
        ('DEVICE_UUID', 'SCHEMA_UUID', 'DISP_NAME', {'property1': 'hoge', 'value1': 'int'},
         {'device_uuid': 'DEVICE_UUID',
          'schema_uuid': 'SCHEMA_UUID',
          'display_name': 'DISP_NAME',
          'properties': {'hoge': 'int'}}),
    ])
    def test_init(self, device_uuid, schema_uuid, display_name, kwargs, expected):
        device = Device(device_uuid, schema_uuid, display_name, **kwargs)
        assert device.uuid == expected['device_uuid']
        assert device.schema_uuid == expected['schema_uuid']
        assert device.display_name == expected['display_name']
        for prop in device.properties:
            assert prop.name in expected['properties']
            assert prop.value == expected['properties'][prop.name]
