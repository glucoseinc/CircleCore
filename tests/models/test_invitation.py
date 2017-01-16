# -*- coding: utf-8 -*-
import datetime

import pytest

from circle_core.models import Invitation


TEST_UUID1 = 'b898884b-19ee-49ef-95c9-f77a4955a54b'
TEST_UUID2 = '25a6aee1-8a19-4f23-83c7-c2acbfb17a30'
# TEST_UUID3 = 'AE2D6831-6255-4953-AD79-5C2E2020B295'


class TestInvitation(object):
    @pytest.mark.parametrize(('uuid', 'max_invites', 'date_created', 'expected'), [
        (TEST_UUID1, '0', None,
         {'uuid': TEST_UUID1,
          'max_invites': 0,
          'date_created': None,
          }),
        (TEST_UUID2, 3, '2008-08-12T12:20:30.656234Z',
         {'uuid': TEST_UUID2,
          'max_invites': 3,
          'date_created': '2008-08-12T12:20:30.656234+00:00'
          }),
    ])
    def test_init(self, uuid, max_invites, date_created, expected):
        user = Invitation(
            uuid, max_invites,
            date_created)

        assert str(user.uuid) == expected['uuid']
        assert user.max_invites == expected['max_invites']

        datestr = user.date_created.isoformat('T') if user.date_created else user.date_created
        assert datestr == expected['date_created']

    @pytest.mark.parametrize(('uuid', 'max_invites', 'date_craeted'), [
        (TEST_UUID1, -1, None),
        (TEST_UUID1, 0, 'hanage'),
    ])
    def test_bad_init(self, uuid, max_invites, date_craeted):
        with pytest.raises(ValueError):
            Invitation(uuid, max_invites, date_craeted)

    def test_is_key_matched(self):
        assert Invitation.is_key_matched('invitation_{}'.format(TEST_UUID1)) is True
        assert Invitation.is_key_matched('schema_{}'.format(TEST_UUID1)) is False
        assert Invitation.is_key_matched('user') is False
        assert Invitation.is_key_matched('user_test_manager@test.test') is False
