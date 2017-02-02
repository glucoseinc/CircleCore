# -*- coding: utf-8 -*-

import re

from click.testing import CliRunner
import pytest

from circle_core.cli import cli_entry
from tests import uuid_rex


class TestCliUser(object):
    @pytest.mark.usefixtures('clear_metadata')
    def test_user(self):
        runner = CliRunner()

        def _call(*args):
            from circle_core.models import MetaDataSession
            MetaDataSession.remove()
            return runner.invoke(cli_entry, ['-c', './tests/circle_core.ini'] + list(args))

        # has no users initialy
        result = _call('user', 'list')
        # import traceback; traceback.print_exception(*result.exc_info)
        # print(result.output)
        assert result.exit_code == 0
        mo = uuid_rex.search(result.output)
        assert mo is None, result.output

        # can add user
        result = _call(
            'user', 'add', '--account', 'test_user', '--password', 'user'
        )
        assert result.exit_code == 0
        mo = uuid_rex.search(result.output)
        assert mo is not None, result.output
        user_uuid = mo.group(1)

        # can list added user
        result = _call('user', 'list')
        assert result.exit_code == 0
        assert user_uuid in result.output

        # can detail added user
        result = _call('user', 'detail', user_uuid)
        assert result.exit_code == 0
        assert user_uuid in result.output
        assert 'test_user' in result.output

        # can fail to remove bad user
        result = _call('user', 'remove', '00000000-0000-0000-0000-000000000000')
        assert result.exit_code != 0

        # can remove user
        result = _call('user', 'remove', user_uuid)
        assert result.exit_code == 0

        # can remove bad user
        result = _call('user', 'list')
        assert result.exit_code == 0
        mo = uuid_rex.search(result.output)
        assert mo is None, result.output
