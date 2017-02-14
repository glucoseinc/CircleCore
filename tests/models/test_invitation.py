# -*- coding: utf-8 -*-
import datetime

import pytest

from circle_core.models import Invitation


TEST_UUID1 = 'b898884b-19ee-49ef-95c9-f77a4955a54b'
TEST_UUID2 = '25a6aee1-8a19-4f23-83c7-c2acbfb17a30'
# TEST_UUID3 = 'AE2D6831-6255-4953-AD79-5C2E2020B295'


@pytest.mark.skip(reason='rewriting...')
class TestInvitation(object):
    @pytest.mark.parametrize(('uuid', 'max_invites', 'created_at', 'expected'), [
        (TEST_UUID1, '0', None,
         {'uuid': TEST_UUID1,
          'max_invites': 0,
          'created_at': None,
          }),
        (TEST_UUID2, 3, '2008-08-12T12:20:30.656234Z',
         {'uuid': TEST_UUID2,
          'max_invites': 3,
          'created_at': '2008-08-12T12:20:30.656234+00:00'
          }),
    ])
    def test_init(self, uuid, max_invites, created_at, expected):
        invitation = Invitation(uuid, max_invites, created_at=created_at)

        assert str(invitation.uuid) == expected['uuid']
        assert invitation.max_invites == expected['max_invites']

        datestr = invitation.created_at.isoformat('T') if invitation.created_at else invitation.created_at
        assert datestr == expected['created_at']

    @pytest.mark.parametrize(('uuid', 'max_invites', 'created_at'), [
        (TEST_UUID1, -1, None),
        (TEST_UUID1, 0, 'hanage'),
    ])
    def test_bad_init(self, uuid, max_invites, created_at):
        with pytest.raises(ValueError):
            Invitation(uuid, max_invites, created_at=created_at)

    def test_is_key_matched(self):
        assert Invitation.is_key_matched('invitation_{}'.format(TEST_UUID1)) is True
        assert Invitation.is_key_matched('schema_{}'.format(TEST_UUID1)) is False
        assert Invitation.is_key_matched('user') is False
        assert Invitation.is_key_matched('user_test_manager@test.test') is False
