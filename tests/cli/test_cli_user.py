# -*- coding: utf-8 -*-

import re

from click.testing import CliRunner
import pytest

from circle_core.cli import cli_entry
from tests import url_scheme_ini_file


class TestCliUser(object):
    @pytest.mark.usefixtures('flushall_redis_server')
    @pytest.mark.parametrize(('main_params', 'expected_output_length'), [
        (['--metadata', url_scheme_ini_file],  # main_params
         1 + 1 + 2),  # expected_output_length

        ([],  # main_params
         1),  # expected_output_length
    ])
    def test_user_list(self, main_params, expected_output_length):
        runner = CliRunner()
        result = runner.invoke(cli_entry, main_params + ['user', 'list'])
        assert result.exit_code == 0
        assert len(result.output.splitlines()) == expected_output_length

    @pytest.mark.parametrize(('main_params', 'user_detail_params', 'expected_exit_code', 'expected_output_length'), [
        (['--metadata', url_scheme_ini_file],  # main_params
         ['3c36ad55-ab76-4027-b86f-0e507656fdaa'],  # user_detail_params test_manager@test.test
         0,  # expected_exit_code
         3),  # expected_output_length

        (['--metadata', url_scheme_ini_file],  # main_params
         ['00000000-0000-0000-0000-000000000000'],  # user_detail_params 登録なし
         -1,  # expected_exit_code
         1),  # expected_output_length
    ])
    def test_user_detail(self, main_params, user_detail_params, expected_exit_code, expected_output_length):
        runner = CliRunner()
        result = runner.invoke(cli_entry, main_params + ['user', 'detail'] + user_detail_params)
        assert result.exit_code == expected_exit_code
        assert len(result.output.splitlines()) == expected_output_length

    @pytest.mark.usefixtures('flushall_redis_server')
    @pytest.mark.parametrize(('main_params', 'user_add_params', 'expected_exit_code', 'expected_output'), [
        (['--metadata', url_scheme_ini_file],  # main_params
         ['--email', 'test_user@test.test', '--password', 'user'],  # user_add_params
         -1,  # expected_exit_code
         'Cannot register to INI File.\n'),  # expected_output

        (['--metadata', 'redis://localhost:65535/16'],  # main_params
         ['--email', 'test_user@test.test', '--password', 'user'],  # user_add_params
         -1,  # expected_exit_code
         'Invalid metadata url / Cannot connect to Redis server. : redis://localhost:65535/16\n'),  # expected_output
    ])
    def test_user_add_failure(self, main_params, user_add_params, expected_exit_code, expected_output):
        runner = CliRunner()
        result = runner.invoke(cli_entry, main_params + ['user', 'add'] + user_add_params)
        assert result.exit_code == expected_exit_code
        assert result.output == expected_output

    @pytest.mark.usefixtures('flushall_redis_server')
    @pytest.mark.parametrize(('user_add_params', 'expected_exit_code', 'expected_output_regexp'), [
        (['--email', 'test_user@test.test', '--password', 'user'],  # user_add_params
         0,
         r'User '
         r'"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}"'  # uuid
         r' is added.\n'),  # expected
    ])
    def test_user_add_success(self, user_add_params, expected_exit_code, expected_output_regexp):
        runner = CliRunner()
        result = runner.invoke(cli_entry, ['user', 'add'] + user_add_params)
        assert result.exit_code == expected_exit_code
        assert re.match(expected_output_regexp, result.output) is not None

    @pytest.mark.usefixtures('flushall_redis_server')
    @pytest.mark.parametrize(('main_params', 'user_remove_params', 'expected_exit_code', 'expected_output'), [
        (['--metadata', url_scheme_ini_file],  # main_params
         ['3c36ad55-ab76-4027-b86f-0e507656fdaa'],  # user_remove_params
         -1,  # expected_exit_code
         'Cannot remove from INI File.\n'),  # expected_output

        ([],  # main_params
         ['00000000-0000-0000-0000-000000000000'],  # user_remove_params
         -1,  # expected_exit_code
         'User "00000000-0000-0000-0000-000000000000" is not registered. Do nothing.\n'),  # expected_output
    ])
    def test_user_remove_failure(self, main_params, user_remove_params, expected_exit_code, expected_output):
        runner = CliRunner()
        result = runner.invoke(cli_entry, main_params + ['user', 'remove'] + user_remove_params)
        assert result.exit_code == expected_exit_code
        assert result.output == expected_output

    @pytest.mark.usefixtures('flushall_redis_server')
    def test_user_remove_success(self):
        # setup
        runner = CliRunner()
        result = runner.invoke(cli_entry, ['user', 'add', '--email', 'test_user@test.test', '--password', 'user'])
        uuid = result.output.split()[1][1:-1]  # User "{uuid}" is added.\n

        # test
        result = runner.invoke(cli_entry, ['user', 'remove', uuid])
        assert result.exit_code == 0
        assert result.output == 'User "{}" is removed.\n'.format(uuid)
