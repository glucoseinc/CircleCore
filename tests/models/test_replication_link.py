# -*- coding: utf-8 -*-
import pytest

from circle_core.models import MessageBox, MetaDataSession, Module, ReplicationLink, Schema, generate_uuid


class TestReplicationLink(object):

    @pytest.mark.parametrize(
        ('_input', 'expected'), [
            (dict(display_name='Link', memo='memo'), dict(display_name='Link', memo='memo')),
        ]
    )
    @pytest.mark.usefixtures('mock_circlecore')
    def test_replication_link(self, _input, expected, mock_circlecore):
        schema = Schema.create(display_name='Schema', properties='x:int,y:float')
        module = Module.create(display_name='Module')

        box = MessageBox(
            uuid=generate_uuid(model=MessageBox), schema_uuid=schema.uuid, module_uuid=module.uuid, display_name='Box'
        )

        with MetaDataSession.begin():
            MetaDataSession.add(schema)
            MetaDataSession.add(module)
            MetaDataSession.add(box)

        replication_link = ReplicationLink.create(message_box_uuids=[box.uuid], **_input)

        with MetaDataSession.begin():
            MetaDataSession.add(replication_link)

        replication_link = ReplicationLink.query.get(replication_link.uuid)
        assert isinstance(replication_link, ReplicationLink)
        assert replication_link.display_name == expected['display_name']
        assert replication_link.memo == expected['memo']
