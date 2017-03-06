# -*- coding: utf-8 -*-
import pytest

from circle_core.models import generate_uuid, MessageBox, MetaDataSession, Module, Schema
from circle_core.models.module import ModuleAttribute, ModuleAttributes

from .utils import setup_db


class TestModule(object):
    @classmethod
    def setup_class(cls):
        setup_db()

    @pytest.mark.parametrize(('_input', 'expected'), [
        (dict(displayName='Module', tags='tag1,tag2,tag3', attributes='attr1:val1,attr2:val2', memo='memo'),
         dict(displayName='Module', tags=['tag1', 'tag2', 'tag3'],
              attributes=[('attr1', 'val1'), ('attr2', 'val2')], memo='memo')),
    ])
    def test_module(self, _input, expected):
        module = Module.create()

        schema = Schema.create(display_name='Schema', properties='x:int,y:float')
        box = MessageBox(uuid=generate_uuid(model=MessageBox),
                         schema_uuid=schema.uuid, module_uuid=module.uuid,
                         display_name='Box')

        _input['messageBoxes'] = [dict(schema=schema.uuid, displayName='Box2', memo='memo')]
        module.update_from_json(_input, with_boxes=True)

        with MetaDataSession.begin():
            MetaDataSession.add(schema)
            MetaDataSession.add(module)
            MetaDataSession.add(box)

        module = Module.query.get(module.uuid)
        assert isinstance(module, Module)
        assert module.display_name == expected['displayName']

        assert isinstance(module.tags, list)
        assert len(module.tags) == len(expected['tags'])
        for tag, exp_tag in zip(module.tags, expected['tags']):
            assert isinstance(tag, str)
            assert tag == exp_tag

        assert isinstance(module.attributes, ModuleAttributes)
        assert len(module.attributes) == len(expected['attributes'])
        for attr, exp_attr in zip(module.attributes, expected['attributes']):
            assert isinstance(attr, ModuleAttribute)
            assert attr.name == exp_attr[0]
            assert attr.value == exp_attr[1]

        assert module.memo == expected['memo']

        assert isinstance(hash(module), int)

        jsonobj = module.to_json(with_boxes=True, with_schema=True, with_cc_info=True)
        assert str(module.uuid) == jsonobj['uuid']
        assert str(module.cc_uuid) == jsonobj['ccUuid']
        assert module.display_name == jsonobj['displayName']
        for tag, json_tag in zip(module.tags, jsonobj['tags']):
            assert tag == json_tag
        for attr, json_attr in zip(module.attributes, jsonobj['attributes']):
            assert attr.name == json_attr['name']
            assert attr.value == json_attr['value']
        assert module.memo == jsonobj['memo']
        assert len(jsonobj['messageBoxes']) == 2
        assert jsonobj['ccInfo']
        assert jsonobj['isReplication'] is False
