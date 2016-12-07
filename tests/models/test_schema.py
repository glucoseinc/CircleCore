# -*- coding: utf-8 -*-
import pytest

from circle_core.models import Schema


TEST_UUID = '550e8400-e29b-41d4-a716-446655440000'


class TestSchema(object):
    @pytest.mark.parametrize(('uuid', 'display_name', 'properties', 'expected'), [
        (TEST_UUID, 'DISP_NAME', 'hoge:int',
         {'uuid': TEST_UUID, 'display_name': 'DISP_NAME', 'properties': {'hoge': 'int'}}),
    ])
    def test_init(self, uuid, display_name, properties, expected):
        schema = Schema(uuid, display_name, properties)
        assert str(schema.uuid) == expected['uuid']
        assert schema.display_name == expected['display_name']
        for prop in schema.properties:
            assert prop.name in expected['properties']
            assert prop.type == expected['properties'][prop.name]
