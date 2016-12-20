# -*- coding: utf-8 -*-
import re

from click.testing import CliRunner
import pytest

from circle_core.cli import cli_entry
from tests import url_scheme_ini_file


class TestCliModule(object):
    @pytest.mark.usefixtures('flushall_redis_server')
    @pytest.mark.parametrize(('main_params', 'expected_output_length'), [
        (['--metadata', url_scheme_ini_file],  # main_params
         1 + 1 + 1),  # expected_output_length

        ([],  # main_params
         1),  # expected_output_length
    ])
    def test_module_list(self, main_params, expected_output_length):
        runner = CliRunner()
        result = runner.invoke(cli_entry, main_params + ['module', 'list'])
        assert result.exit_code == 0
        len(result.output.splitlines()) == expected_output_length

    @pytest.mark.parametrize(('main_params', 'module_detail_params', 'expected_exit_code', 'expected_output_length'), [
        (['--metadata', url_scheme_ini_file],  # main_params
         ['838c8a6d-4946-4715-ae4b-39d0d64884fb'],  # schema_detail_params 温度センサデバイス1
         0,  # expected_exit_code
         1 + 1 + 1 + 3 + 1 + 1 + 1 + 1 + 1 + 1),  # expected_output_length

        (['--metadata', url_scheme_ini_file],  # main_params
         ['00000000-0000-0000-0000-000000000000'],  # schema_detail_params 登録なし
         -1,  # expected_exit_code
         1),  # expected_output_length
    ])
    def test_module_detail(self, main_params, module_detail_params, expected_exit_code, expected_output_length):
        runner = CliRunner()
        result = runner.invoke(cli_entry, main_params + ['module', 'detail'] + module_detail_params)
        assert result.exit_code == expected_exit_code
        assert len(result.output.splitlines()) == expected_output_length

    @pytest.mark.usefixtures('flushall_redis_server')
    @pytest.mark.parametrize(('main_params', 'module_add_params', 'expected_exit_code', 'expected_output'), [
        (['--metadata', url_scheme_ini_file],  # main_params
         ['--name', '温度センサデバイス2',
          '--box', 'a4c81b94-b03d-4649-927b-e3b1d259eaa2',
          '--tag', 'tag1,tag2'],  # module_add_params
         -1,  # expected_exit_code
         'Cannot register to INI File.\n'),  # expected_output

        ([],  # main_params
         ['--name', '温度センサデバイス2',
          '--box', '00000000-0000-0000-0000-000000000000',
          '--tag', 'tag1,tag2'],  # module_add_params
         -1,  # expected_exit_code
         'MessageBox "00000000-0000-0000-0000-000000000000" is not exist. Do nothing.\n'),  # expected_output
    ])
    def test_module_add_failure(self, main_params, module_add_params, expected_exit_code, expected_output):
        runner = CliRunner()
        result = runner.invoke(cli_entry, main_params + ['module', 'add'] + module_add_params)
        assert result.exit_code == expected_exit_code
        assert result.output == expected_output

    @pytest.mark.usefixtures('flushall_redis_server')
    def test_module_add_success(self):
        # setup
        runner = CliRunner()
        result = runner.invoke(cli_entry, ['schema', 'add', 'key:int'])
        schema_uuid = result.output.split()[1][1:-1]  # Schema "{uuid}" is added.\n

        result = runner.invoke(cli_entry, ['box', 'add', '--schema', schema_uuid])
        message_box_uuid = result.output.split()[1][1:-1]  # MessageBox "{uuid}" is added.\n

        # test
        module_add_params = ['--name', 'module_name',
                             '--box', message_box_uuid,
                             '--tag', 'tag1,tag2,tag3']
        expected_output_regexp = r'Module ' \
                                 r'"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}"' \
                                 r' is added.\n'
        result = runner.invoke(cli_entry, ['module', 'add'] + module_add_params)
        assert result.exit_code == 0
        assert re.match(expected_output_regexp, result.output) is not None

    @pytest.mark.usefixtures('flushall_redis_server')
    @pytest.mark.parametrize(('main_params', 'module_remove_params', 'expected_exit_code', 'expected_output'), [
        (['--metadata', url_scheme_ini_file],  # main_params
         ['838c8a6d-4946-4715-ae4b-39d0d64884fb'],  # module_remove_params
         -1,  # expected_exit_code
         'Cannot remove from INI File.\n'),  # expected_output

        ([],  # main_params
         ['00000000-0000-0000-0000-000000000000'],  # module_remove_params
         -1,  # expected_exit_code
         'Module "00000000-0000-0000-0000-000000000000" is not registered. Do nothing.\n'),  # expected_output
    ])
    def test_module_remove_failure(self, main_params, module_remove_params, expected_exit_code, expected_output):
        runner = CliRunner()
        result = runner.invoke(cli_entry, main_params + ['module', 'remove'] + module_remove_params)
        assert result.exit_code == expected_exit_code
        assert result.output == expected_output

    @pytest.mark.usefixtures('flushall_redis_server')
    def test_module_remove_success(self):
        # setup
        runner = CliRunner()
        result = runner.invoke(cli_entry, ['schema', 'add', 'key:int'])
        schema_uuid = result.output.split()[1][1:-1]  # Schema "{uuid}" is added.\n

        result = runner.invoke(cli_entry, ['box', 'add', '--schema', schema_uuid])
        message_box_uuid = result.output.split()[1][1:-1]  # MessageBox "{uuid}" is added.\n

        module_add_params = ['--name', 'module_name',
                             '--box', message_box_uuid,
                             '--tag', 'tag1,tag2,tag3']
        result = runner.invoke(cli_entry, ['module', 'add'] + module_add_params)
        module_uuid = result.output.split()[1][1:-1]  # Module "{uuid}" is added.\n

        # test
        result = runner.invoke(cli_entry, ['module', 'remove', module_uuid])
        assert result.exit_code == 0
        assert result.output == 'Module "{}" is removed.\n'.format(module_uuid)
