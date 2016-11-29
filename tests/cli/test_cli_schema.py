# -*- coding: utf-8 -*-

import re

from click.testing import CliRunner
import pytest

from circle_core.cli import cli_main
from tests import url_scheme_ini_file


class TestCliSchema(object):
    @pytest.mark.usefixtures('flushall_redis_server')
    @pytest.mark.parametrize(('main_params', 'expected_output_length'), [
        (['--config', url_scheme_ini_file],  # main_params
         1 + 1 + 2 + 1),  # expected_output_length

        ([],  # main_params
         1 + 1),  # expected_output_length
    ])
    def test_schema_list(self, main_params, expected_output_length):
        runner = CliRunner()
        result = runner.invoke(cli_main, main_params + ['schema', 'list'])
        assert result.exit_code == 0
        assert len(result.output.split('\n')) == expected_output_length

    @pytest.mark.parametrize(('main_params', 'schema_detail_params', 'expected_exit_code', 'expected_output_length'), [
        (['--config', url_scheme_ini_file],  # main_params
         ['32218d0b-ad2a-4316-843b-4217fc2deb0b'],  # schema_detail_params 温度センサ
         0,  # expected_exit_code
         1 + 1 + 5 + 1 + 1),  # expected_output_length

        (['--config', url_scheme_ini_file],  # main_params
         ['00000000-0000-0000-0000-000000000000'],  # schema_detail_params 登録なし
         -1,  # expected_exit_code
         1 + 1),  # expected_output_length

        (['--config', url_scheme_ini_file],  # main_params
         ['7c6b4c74-43f2-493d-9d33-8e460047fccd'],  # schema_detail_params 湿度センサ
         0,  # expected_exit_code
         1 + 1 + 5 + 1 + 1),  # expected_output_length
    ])
    def test_schema_detail(self, main_params, schema_detail_params, expected_exit_code, expected_output_length):
        runner = CliRunner()
        result = runner.invoke(cli_main, main_params + ['schema', 'detail'] + schema_detail_params)
        assert result.exit_code == expected_exit_code
        assert len(result.output.split('\n')) == expected_output_length

    @pytest.mark.usefixtures('flushall_redis_server')
    @pytest.mark.parametrize(('main_params', 'schema_add_params', 'expected_exit_code', 'expected_output'), [
        (['--config', url_scheme_ini_file],  # main_params
         ['--name', 'schema_name', 'key:int'],  # schema_add_params
         -1,  # expected_exit_code
         'Cannot register to INI File.\n'),  # expected_output

        (['--config', 'redis://localhost:65535/16'],  # main_params
         ['--name', 'schema_name', 'key:int'],  # schema_add_params
         -1,  # expected_exit_code
         'Invalid config url / Cannot connect to Redis server. : redis://localhost:65535/16\n'),  # expected_output

        ([],  # main_params
         ['--name', 'schema_name', 'key_int'],  # schema_add_params
         -1,  # expected_exit_code
         'Argument is invalid : key_int.\nArgument format must be "name:type".\n'),  # expected_output
    ])
    def test_schema_add_failure(self, main_params, schema_add_params, expected_exit_code, expected_output):
        runner = CliRunner()
        result = runner.invoke(cli_main, main_params + ['schema', 'add'] + schema_add_params)
        assert result.exit_code == expected_exit_code
        assert result.output == expected_output

    @pytest.mark.usefixtures('flushall_redis_server')
    @pytest.mark.parametrize(('schema_add_params', 'expected_exit_code', 'expected_output_regexp'), [
        (['--name', 'schema_name', 'key:int'],  # schema_add_params
         0,
         r'Schema '
         r'"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}"'  # uuid
         r' is added.\n'),  # expected
    ])
    def test_schema_add_success(self, schema_add_params, expected_exit_code, expected_output_regexp):
        runner = CliRunner()
        result = runner.invoke(cli_main, ['schema', 'add'] + schema_add_params)
        assert result.exit_code == expected_exit_code
        assert re.match(expected_output_regexp, result.output) is not None

    @pytest.mark.usefixtures('flushall_redis_server')
    @pytest.mark.parametrize(('main_params', 'schema_remove_params', 'expected_exit_code', 'expected_output'), [
        (['--config', url_scheme_ini_file],  # main_params
         ['32218d0b-ad2a-4316-843b-4217fc2deb0b'],  # schema_remove_params
         -1,  # expected_exit_code
         'Cannot remove from INI File.\n'),  # expected_output

        ([],  # main_params
         ['00000000-0000-0000-0000-000000000000'],  # schema_remove_params
         -1,  # expected_exit_code
         'Schema "00000000-0000-0000-0000-000000000000" is not registered. Do nothing.\n'),  # expected_output
    ])
    def test_schema_remove_failure(self, main_params, schema_remove_params, expected_exit_code, expected_output):
        runner = CliRunner()
        result = runner.invoke(cli_main, main_params + ['schema', 'remove'] + schema_remove_params)
        assert result.exit_code == expected_exit_code
        assert result.output == expected_output

    @pytest.mark.usefixtures('flushall_redis_server')
    def test_schema_remove_success(self):
        # setup
        runner = CliRunner()
        result = runner.invoke(cli_main, ['schema', 'add', 'key:int'])
        uuid = result.output.split()[1][1:-1]  # Schema "{uuid}" is added.\n

        # test
        result = runner.invoke(cli_main, ['schema', 'remove', uuid])
        assert result.exit_code == 0
        assert result.output == 'Schema "{}" is removed.\n'.format(uuid)
