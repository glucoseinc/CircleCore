# -*- coding: utf-8 -*-
import uuid

import pytest

from circle_core.models import MessageBox, MetaDataSession, Module, Schema, generate_uuid


class TestMessageBox(object):

    @pytest.mark.parametrize(
        ('_input', 'expected'),
        [
            (dict(display_name='MessageBox', memo='memo'), dict(display_name='MessageBox', memo='memo')),
        ]
    )
    @pytest.mark.usefixtures('mock_circlecore')
    def test_message_box(self, _input, expected, mock_circlecore):
        schema = Schema.create(display_name='Schema', properties='x:int,y:float')
        module = Module.create(display_name='Module')

        box = MessageBox(
            uuid=generate_uuid(model=MessageBox), schema_uuid=schema.uuid, module_uuid=module.uuid, **_input
        )

        with MetaDataSession.begin():
            MetaDataSession.add(schema)
            MetaDataSession.add(module)
            MetaDataSession.add(box)

        box = MessageBox.query.get(box.uuid)
        assert isinstance(box, MessageBox)
        assert box.display_name == expected['display_name']
        assert box.memo == expected['memo']

        assert isinstance(hash(box), int)
        assert isinstance(box.cc_uuid, uuid.UUID)

        jsonobj = box.to_json(with_schema=True, with_module=True)
        assert str(box.uuid) == jsonobj['uuid']
        assert box.display_name == jsonobj['displayName']
        assert box.memo == jsonobj['memo']
        assert str(box.module_uuid) == jsonobj['moduleUuid']
        assert str(box.schema_uuid) == jsonobj['schemaUuid']
        assert schema.display_name == jsonobj['schema']['displayName']
        assert module.display_name == jsonobj['module']['displayName']

    @pytest.mark.parametrize(('_input', 'expected'), [  # noqa: F811
        (
            dict(displayName='MessageBoxUpdate', memo='memoUpdate'),
            dict(display_name='MessageBoxUpdate', memo='memoUpdate')
        ),
    ])
    def test_update_from_json(self, _input, expected, mock_circlecore):
        schema = Schema.create(display_name='Schema', properties='x:int,y:float')
        module = Module.create(display_name='Module')
        box = MessageBox(
            uuid=generate_uuid(model=MessageBox),
            schema_uuid=schema.uuid,
            module_uuid=module.uuid,
            display_name='MessageBoxOldName'
        )
        with MetaDataSession.begin():
            MetaDataSession.add(schema)
            MetaDataSession.add(module)
            MetaDataSession.add(box)

        box = MessageBox.query.get(box.uuid)
        box.update_from_json(_input)
        with MetaDataSession.begin():
            MetaDataSession.add(box)

        box = MessageBox.query.get(box.uuid)
        assert isinstance(box, MessageBox)
        assert box.display_name == expected['display_name']
        assert box.memo == expected['memo']
