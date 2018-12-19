# -*- coding: utf-8 -*-
import pytest

from circle_core.models import generate_uuid, MessageBox, MetaDataSession, Module, Schema, SchemaProperties
from circle_core.models.schema import SchemaProperty
from circle_core.testing import setup_db


class TestSchema(object):

    @classmethod
    def setup_class(cls):
        setup_db()

    @pytest.mark.parametrize(('_input', 'expected'), [
        (
            dict(displayName='Schema', memo='memo', properties='x:int,y:float'),
            dict(displayName='Schema', memo='memo', properties=[('x', 'int'), ('y', 'float')])
        ),
    ])
    def test_schema(self, _input, expected):
        schema = Schema.create()
        schema.update_from_json(_input)

        module = Module.create(display_name='Module')
        box = MessageBox(
            uuid=generate_uuid(model=MessageBox), schema_uuid=schema.uuid, module_uuid=module.uuid, display_name='Box'
        )

        with MetaDataSession.begin():
            MetaDataSession.add(schema)
            MetaDataSession.add(module)
            MetaDataSession.add(box)

        schema = Schema.query.get(schema.uuid)
        assert isinstance(schema, Schema)
        assert schema.display_name == expected['displayName']
        assert schema.memo == expected['memo']

        assert isinstance(schema.properties, SchemaProperties)
        assert len(schema.properties) == len(expected['properties'])
        for prop, exp_prop in zip(schema.properties, expected['properties']):
            assert isinstance(prop, SchemaProperty)
            assert prop.name == exp_prop[0]
            assert prop.type == exp_prop[1]

        assert isinstance(hash(schema), int)

        jsonobj = schema.to_json(with_modules=True)
        assert str(schema.uuid) == jsonobj['uuid']
        assert str(schema.cc_uuid) == jsonobj['ccUuid']
        assert schema.display_name == jsonobj['displayName']
        for prop, json_prop in zip(schema.properties, jsonobj['properties']):
            assert prop.name == json_prop['name']
            assert prop.type == json_prop['type']
        assert schema.memo == jsonobj['memo']

        assert len(jsonobj['modules']) == 1
        assert module.display_name == jsonobj['modules'][0]['displayName']

    @pytest.mark.parametrize(('_input', 'data', 'expected'), [
        (
            'a:int,b:float,c:bool,d:string,e:bytes,f:date,g:datetime,h:time,i:timestamp',
            dict(
                a=1,
                b=1.0,
                c=True,
                d='String',
                e='Bytes',
                f='20170101',
                g='2017-01-01 00:00:00',
                h='00:00:00',
                i='1970-01-01 00:00:01'
            ), True
        ),
        ('a:int,b:float', dict(a=1), False),
        ('a:int', dict(x=1), False),
    ])
    def test_check_match(self, _input, data, expected):
        jsonobj = dict(displayName='Schema', memo='memo', properties=_input)
        schema = Schema.create()
        schema.update_from_json(jsonobj)

        with MetaDataSession.begin():
            MetaDataSession.add(schema)

        schema = Schema.query.get(schema.uuid)
        assert schema.check_match(data) is expected
