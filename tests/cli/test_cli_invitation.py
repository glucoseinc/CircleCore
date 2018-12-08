# -*- coding: utf-8 -*-

import re

from click.testing import CliRunner
import pytest

from circle_core.cli import cli_entry
from tests import uuid_rex


@pytest.mark.skip(reason='rewriting...')
class TestCliInvitation(object):

    @pytest.mark.usefixtures('clear_metadata')
    def test_invitation(self):
        runner = CliRunner()

        def _call(*args):
            from circle_core.models import MetaDataSession
            MetaDataSession.remove()
            return runner.invoke(cli_entry, ['-c', './tests/circle_core.ini', 'invitation'] + list(args))

        # has no user
        result = _call('list')
        assert result.exit_code == 0
        mo = uuid_rex.search(result.output)
        assert mo is None, result.output

        # can add invitation
        result = _call('add')
        assert result.exit_code == 0
        mo = uuid_rex.search(result.output)
        assert mo is not None, result.output
        invitation_uuid = mo.group(1)

        # can list added invitation
        result = _call('list')
        assert result.exit_code == 0
        assert invitation_uuid in result.output

        # can detail added inviation
        result = _call('detail', invitation_uuid)
        assert result.exit_code == 0
        assert invitation_uuid in result.output

        # can fail to remove bad invitation
        result = _call('remove', '00000000-0000-0000-0000-000000000000')
        assert result.exit_code != 0

        # can remove invitation
        result = _call('remove', invitation_uuid)
        assert result.exit_code == 0

        # can list
        result = _call('list')
        assert result.exit_code == 0
        mo = uuid_rex.search(result.output)
        assert mo is None, result.output
