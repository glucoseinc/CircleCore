# -*- coding: utf-8 -*-
import pytest

from circle_core.models.device import Device


TEST_DEVICE_UUID = '00000000-0000-0000-0000-000000000000'
TEST_SCHEMA_UUID = '00000000-0000-0000-0000-000000000001'


class TestDevice(object):
    @pytest.mark.parametrize(('device_uuid', 'schema_uuid', 'display_name', 'kwargs', 'expected'), [
        (TEST_DEVICE_UUID, TEST_SCHEMA_UUID, 'DISP_NAME', {'property1': 'hoge', 'value1': 'int'},
         {'device_uuid': TEST_DEVICE_UUID,
          'schema_uuid': TEST_SCHEMA_UUID,
          'display_name': 'DISP_NAME',
          'properties': {'hoge': 'int'}}),
    ])
    def test_init(self, device_uuid, schema_uuid, display_name, kwargs, expected):
        device = Device(device_uuid, schema_uuid, display_name, **kwargs)
        assert str(device.uuid) == expected['device_uuid']
        assert str(device.schema_uuid) == expected['schema_uuid']
        assert device.display_name == expected['display_name']
        for prop in device.properties:
            assert prop.name in expected['properties']
            assert prop.value == expected['properties'][prop.name]
