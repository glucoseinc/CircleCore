# -*- coding: utf-8 -*-

import re

from click.testing import CliRunner
import pytest

from circle_core.cli import cli_entry
from tests import url_scheme_ini_file


class TestCliInvitation(object):
    @pytest.mark.usefixtures('flushall_redis_server')
    @pytest.mark.parametrize(('main_params', 'expected_output_length'), [
        (['--metadata', url_scheme_ini_file],  # main_params
         1 + 1 + 2),  # expected_output_length

        ([],  # main_params
         1),  # expected_output_length
    ])
    def test_invitation_list(self, main_params, expected_output_length):
        runner = CliRunner()
        result = runner.invoke(cli_entry, main_params + ['invitation', 'list'])
        assert result.exit_code == 0
        assert len(result.output.splitlines()) == expected_output_length

    @pytest.mark.parametrize(('main_params', 'detail_params', 'expected_exit_code', 'expected_output_length'), [
        (['--metadata', url_scheme_ini_file],  # main_params
         ['b898884b-19ee-49ef-95c9-f77a4955a54b'],  # detail_params test_manager@test.test
         0,  # expected_exit_code
         4),  # expected_output_length

        (['--metadata', url_scheme_ini_file],  # main_params
         ['00000000-0000-0000-0000-000000000000'],  # detail_params 登録なし
         255,  # expected_exit_code
         1),  # expected_output_length
    ])
    def test_invitation_detail(self, main_params, detail_params, expected_exit_code, expected_output_length):
        runner = CliRunner()
        result = runner.invoke(cli_entry, main_params + ['invitation', 'detail'] + detail_params)
        assert result.exit_code == expected_exit_code
        assert len(result.output.splitlines()) == expected_output_length

    @pytest.mark.usefixtures('flushall_redis_server')
    @pytest.mark.parametrize(('main_params', 'add_params', 'expected_exit_code', 'expected_output'), [
        (['--metadata', url_scheme_ini_file],  # main_params
         ['--max', '3'],  # add_params
         -1,  # expected_exit_code
         'Cannot register to INI File.\n'),  # expected_output

        (['--metadata', 'redis://localhost:65535/16'],  # main_params
         ['--max', '0'],  # add_params
         -1,  # expected_exit_code
         'Invalid metadata url / Cannot connect to Redis server. : redis://localhost:65535/16\n'),  # expected_output
    ])
    def test_invitation_add_failure(self, main_params, add_params, expected_exit_code, expected_output):
        runner = CliRunner()
        result = runner.invoke(cli_entry, main_params + ['invitation', 'add'] + add_params)
        assert result.exit_code == expected_exit_code
        assert result.output == expected_output

    @pytest.mark.usefixtures('flushall_redis_server')
    @pytest.mark.parametrize(('add_params', 'expected_exit_code', 'expected_output_regexp'), [
        (['--max', '4'],  # add_params
         0,
         r'Invitation '
         r'"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}"'  # uuid
         r' is added.\n'),  # expected
    ])
    def test_invitation_add_success(self, add_params, expected_exit_code, expected_output_regexp):
        runner = CliRunner()
        result = runner.invoke(cli_entry, ['invitation', 'add'] + add_params)
        assert result.exit_code == expected_exit_code
        assert re.match(expected_output_regexp, result.output) is not None

    @pytest.mark.usefixtures('flushall_redis_server')
    @pytest.mark.parametrize(('main_params', 'remove_params', 'expected_exit_code', 'expected_output'), [
        (['--metadata', url_scheme_ini_file],  # main_params
         ['b898884b-19ee-49ef-95c9-f77a4955a54b'],  # remove_params
         -1,  # expected_exit_code
         'Cannot remove from INI File.\n'),  # expected_output

        ([],  # main_params
         ['00000000-0000-0000-0000-000000000000'],  # remove_params
         -1,  # expected_exit_code
         'Invitation "00000000-0000-0000-0000-000000000000" is not registered. Do nothing.\n'),  # expected_output
    ])
    def test_invitation_remove_failure(self, main_params, remove_params, expected_exit_code, expected_output):
        runner = CliRunner()
        result = runner.invoke(cli_entry, main_params + ['invitation', 'remove'] + remove_params)
        assert result.exit_code == expected_exit_code
        assert result.output == expected_output

    @pytest.mark.usefixtures('flushall_redis_server')
    def test_invitation_remove_success(self):
        # setup
        runner = CliRunner()
        result = runner.invoke(cli_entry, ['invitation', 'add', '--max', '9999'])
        uuid = result.output.split()[1][1:-1]  # User "{uuid}" is added.\n

        # test
        result = runner.invoke(cli_entry, ['invitation', 'remove', uuid])
        assert result.exit_code == 0
        assert result.output == 'Invitation "{}" is removed.\n'.format(uuid)
