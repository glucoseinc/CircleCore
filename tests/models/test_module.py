# -*- coding: utf-8 -*-
import pytest

from circle_core.models.module import Module


TEST_MODULE_UUID = '00000000-0000-0000-0000-000000000000'
TEST_SCHEMA_UUID = '00000000-0000-0000-0000-000000000001'


class TestModule(object):
    @pytest.mark.parametrize(('module_uuid', 'schema_uuid', 'display_name', 'properties', 'expected'), [
        (TEST_MODULE_UUID, TEST_SCHEMA_UUID, 'DISP_NAME', 'test_name:test_value',
         {'module_uuid': TEST_MODULE_UUID,
          'schema_uuid': TEST_SCHEMA_UUID,
          'display_name': 'DISP_NAME',
          'properties': {'test_name': 'test_value'}}),
    ])
    def test_init(self, module_uuid, schema_uuid, display_name, properties, expected):
        module = Module(module_uuid, schema_uuid, display_name, properties)
        assert str(module.uuid) == expected['module_uuid']
        assert str(module.schema_uuid) == expected['schema_uuid']
        assert module.display_name == expected['display_name']
        for prop in module.properties:
            assert prop.name in expected['properties']
            assert prop.value == expected['properties'][prop.name]
