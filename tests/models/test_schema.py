# -*- coding: utf-8 -*-
from uuid import uuid4

import pytest

from circle_core.models import Schema


TEST_UUID = '550e8400-e29b-41d4-a716-446655440000'


class TestSchema(object):
    @pytest.mark.parametrize(('uuid', 'display_name', 'stringified_properties', 'expected'), [
        (TEST_UUID, 'DISP_NAME', 'prop1:int,prop2:float',
         {'uuid': TEST_UUID, 'display_name': 'DISP_NAME', 'properties': {'prop1': 'int', 'prop2': 'float'}}),
    ])
    def test_init(self, uuid, display_name, stringified_properties, expected):
        dictified_properties = Schema.dictify_properties(stringified_properties)
        schema = Schema(uuid, display_name, dictified_properties)
        assert str(schema.uuid) == expected['uuid']
        assert schema.display_name == expected['display_name']
        for prop in schema.properties:
            assert prop.name in expected['properties']
            assert prop.type == expected['properties'][prop.name]
