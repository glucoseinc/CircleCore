# -*- coding: utf-8 -*-
import pytest

from circle_core.models import generate_uuid, Invitation, MetaDataSession
from circle_core.testing import setup_db


class TestInvitation(object):

    @classmethod
    def setup_class(cls):
        setup_db()

    @pytest.mark.parametrize(
        ('_input', 'expected'), [
            (dict(max_invites=10), dict(max_invites=10, current_invites=0)),
        ]
    )
    def test_invitation(self, _input, expected):
        invitation = Invitation(uuid=generate_uuid(model=Invitation), **_input)

        with MetaDataSession.begin():
            MetaDataSession.add(invitation)

        invitation = Invitation.query.get(invitation.uuid)
        assert isinstance(invitation, Invitation)
        assert invitation.max_invites == expected['max_invites']
        assert invitation.current_invites == expected['current_invites']

        for i in range(_input['max_invites']):
            assert invitation.can_invite() is True
            invitation.inc_invites()
        else:
            assert invitation.can_invite() is False
