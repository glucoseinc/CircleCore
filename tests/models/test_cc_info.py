# -*- coding: utf-8 -*-
import pytest

from circle_core.models import CcInfo, MetaDataSession
from circle_core.testing import setup_db


class TestCcInfo(object):
    @classmethod
    def setup_class(cls):
        setup_db()

    @pytest.mark.parametrize(('_input', 'expected'), [
        (dict(display_name='OtherCircleCore', uuid='EEEEEEEE-EEEE-4EEE-EEEE-EEEEEEEEEEEE', myself=False, work='Other'),
         dict(display_name='OtherCircleCore', uuid='EEEEEEEE-EEEE-4EEE-EEEE-EEEEEEEEEEEE', myself=False, work='Other')),
    ])
    def test_cc_info(self, _input, expected):
        other_cc_info = CcInfo(**_input)
        with MetaDataSession.begin():
            MetaDataSession.add(other_cc_info)

        own_cc_info = CcInfo.query.filter_by(myself=True).all()
        assert len(own_cc_info) == 1

        other_cc_info = CcInfo.query.get(_input['uuid'])
        assert isinstance(other_cc_info, CcInfo)
        assert other_cc_info.display_name == expected['display_name']
        assert str(other_cc_info.uuid).lower() == expected['uuid'].lower()
        assert other_cc_info.myself == expected['myself']
        assert other_cc_info.work == expected['work']

        jsonobj = other_cc_info.to_json()
        assert str(other_cc_info.uuid) == jsonobj['uuid']
        assert other_cc_info.display_name == jsonobj['displayName']
        assert other_cc_info.work == jsonobj['work']
        assert other_cc_info.myself == jsonobj['myself']
