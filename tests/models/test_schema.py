# -*- coding: utf-8 -*-

from circle_core.models.schema import Schema
import pytest


class TestSchema(object):
    @pytest.mark.parametrize(('uuid', 'display_name', 'kwargs', 'expected'), [
        ('UUID', 'DISP_NAME', {'key1': 'hoge', 'type1': 'int'},
         {'uuid': 'UUID', 'display_name': 'DISP_NAME', 'properties': {'hoge': 'int'}}),
    ])
    def test_init(self, uuid, display_name, kwargs, expected):
        schema = Schema(uuid, display_name, **kwargs)
        assert schema.uuid == expected['uuid']
        assert schema.display_name == expected['display_name']
        for prop in schema.properties:
            assert prop.name in expected['properties']
            assert prop.type == expected['properties'][prop.name]
