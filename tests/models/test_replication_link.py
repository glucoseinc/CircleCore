# -*- coding: utf-8 -*-
import pytest

from circle_core.models import generate_uuid, MessageBox, MetaDataSession, Module, ReplicationLink, Schema
from circle_core.testing import setup_db


class TestReplicationLink(object):
    @classmethod
    def setup_class(cls):
        setup_db()

    @pytest.mark.parametrize(('_input', 'expected'), [
        (dict(display_name='Link', memo='memo'),
         dict(display_name='Link', memo='memo')),
    ])
    def test_replication_link(self, _input, expected):
        schema = Schema.create(display_name='Schema', properties='x:int,y:float')
        module = Module.create(display_name='Module')

        box = MessageBox(uuid=generate_uuid(model=MessageBox),
                         schema_uuid=schema.uuid, module_uuid=module.uuid,
                         display_name='Box')

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
