# -*- coding: utf-8 -*-
import pytest

from circle_core.models import Module


TEST_MODULE_UUID = '00000000-0000-0000-0000-000000000000'
TEST_MESSAGE_BOX_UUID1 = '00000000-0000-0000-0000-000000000001'
TEST_MESSAGE_BOX_UUID2 = '00000000-0000-0000-0000-000000000002'


class TestModule(object):
    @pytest.mark.parametrize(('module_uuid', 'message_box_uuids', 'display_name', 'tags', 'expected'), [
        (TEST_MODULE_UUID,
         ','.join([TEST_MESSAGE_BOX_UUID1, TEST_MESSAGE_BOX_UUID2]),
         'DISP_NAME',
         'test_tag1,test_tag2',
         {'module_uuid': TEST_MODULE_UUID,
          'message_box_uuids': [TEST_MESSAGE_BOX_UUID1, TEST_MESSAGE_BOX_UUID2],
          'display_name': 'DISP_NAME',
          'tags': ['test_tag1', 'test_tag2']}),
    ])
    def test_init(self, module_uuid, message_box_uuids, display_name, tags, expected):
        module = Module(module_uuid, message_box_uuids, display_name, tags)
        assert str(module.uuid) == expected['module_uuid']
        for (message_box_uuid, expected_value) in zip(module.message_box_uuids, expected['message_box_uuids']):
            assert str(message_box_uuid) == expected_value
        assert module.display_name == expected['display_name']
        for (tag, expected_value) in zip(module.tags, expected['tags']):
            assert tag == expected_value
