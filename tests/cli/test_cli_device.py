#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

from circle_core.cli import cli_main
from click.testing import CliRunner
import pytest

from tests import flushall_redis_server, redis_server, url_scheme_ini_file


class TestCliDevice(object):
    @pytest.mark.usefixtures('flushall_redis_server')
    @pytest.mark.parametrize(('main_params', 'expected_output_length'), [
        (['--config', url_scheme_ini_file],  # main_params
         1 + 1 + 1 + 1),  # expected_output_length

        ([],  # main_params
         1 + 1),  # expected_output_length
    ])
    def test_device_list(self, main_params, expected_output_length):
        runner = CliRunner()
        result = runner.invoke(cli_main, main_params + ['device', 'list'])
        assert result.exit_code == 0
        len(result.output.split('\n')) == expected_output_length

    @pytest.mark.parametrize(('main_params', 'device_detail_params', 'expected_exit_code', 'expected_output_length'), [
        (['--config', url_scheme_ini_file],  # main_params
         ['838c8a6d-4946-4715-ae4b-39d0d64884fb'],  # schema_detail_params 温度センサデバイス1
         0,  # expected_exit_code
         1 + 1 + 1 + 2 + 1),  # expected_output_length

        (['--config', url_scheme_ini_file],  # main_params
         ['00000000-0000-0000-0000-000000000000'],  # schema_detail_params 登録なし
         -1,  # expected_exit_code
         1 + 1),  # expected_output_length
    ])
    def test_device_detail(self, main_params, device_detail_params, expected_exit_code, expected_output_length):
        runner = CliRunner()
        result = runner.invoke(cli_main, main_params + ['device', 'detail'] + device_detail_params)
        assert result.exit_code == expected_exit_code
        assert len(result.output.split('\n')) == expected_output_length

    @pytest.mark.usefixtures('flushall_redis_server')
    @pytest.mark.parametrize(('main_params', 'device_add_params', 'expected_exit_code', 'expected_output'), [
        (['--config', url_scheme_ini_file],  # main_params
         ['--name', '温度センサデバイス2',
          '--schema', '32218d0b-ad2a-4316-843b-4217fc2deb0b',
          '--property', 'name:P002,type:temperature'],  # device_add_params
         -1,  # expected_exit_code
         'Cannot register to INI File.\n'),  # expected_output

        ([],  # main_params
         ['--name', '温度センサデバイス2',
          '--schema', '00000000-0000-0000-0000-000000000000',
          '--property', 'name:P002,type:temperature'],  # device_add_params
         -1,  # expected_exit_code
         'Schema "00000000-0000-0000-0000-000000000000" is not exist. Do nothing.\n'),  # expected_output
    ])
    def test_device_add_failure(self, main_params, device_add_params, expected_exit_code, expected_output):
        runner = CliRunner()
        result = runner.invoke(cli_main, main_params + ['device', 'add'] + device_add_params)
        assert result.exit_code == expected_exit_code
        assert result.output == expected_output

    @pytest.mark.usefixtures('flushall_redis_server')
    def test_device_add_failure_invalid_argument(self):
        # setup
        runner = CliRunner()
        result = runner.invoke(cli_main, ['schema', 'add', 'key:int'])
        schema_uuid = result.output.split()[1][1:-1]  # Schema "{uuid}" is added.\n

        # test
        device_add_params = ['--name', 'device_name',
                             '--schema', schema_uuid,
                             '--property', 'name=new_device,group=k_dai']
        expected_output = 'Argument "property" is invalid : name=new_device. Do nothing.\n' \
                          'Argument "property" format must be "name1:type1,name2:type2...".\n'
        result = runner.invoke(cli_main, ['device', 'add'] + device_add_params)
        assert result.exit_code == -1
        assert result.output == expected_output

    @pytest.mark.usefixtures('flushall_redis_server')
    def test_device_add_success(self):
        # setup
        runner = CliRunner()
        result = runner.invoke(cli_main, ['schema', 'add', 'key:int'])
        schema_uuid = result.output.split()[1][1:-1]  # Schema "{uuid}" is added.\n

        # test
        device_add_params = ['--name', 'device_name',
                             '--schema', schema_uuid,
                             '--property', 'name:new_device,group:k_dai']
        expected_output_regexp = r'Device ' \
                                 r'"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}"' \
                                 r' is added.\n'
        result = runner.invoke(cli_main, ['device', 'add'] + device_add_params)
        assert result.exit_code == 0
        assert re.match(expected_output_regexp, result.output) is not None

    @pytest.mark.usefixtures('flushall_redis_server')
    @pytest.mark.parametrize(('main_params', 'device_remove_params', 'expected_exit_code', 'expected_output'), [
        (['--config', url_scheme_ini_file],  # main_params
         ['838c8a6d-4946-4715-ae4b-39d0d64884fb'],  # device_remove_params
         -1,  # expected_exit_code
         'Cannot remove from INI File.\n'),  # expected_output

        ([],  # main_params
         ['00000000-0000-0000-0000-000000000000'],  # device_remove_params
         -1,  # expected_exit_code
         'Device "00000000-0000-0000-0000-000000000000" is not registered. Do nothing.\n'),  # expected_output
    ])
    def test_device_remove_failure(self, main_params, device_remove_params, expected_exit_code, expected_output):
        runner = CliRunner()
        result = runner.invoke(cli_main, main_params + ['device', 'remove'] + device_remove_params)
        assert result.exit_code == expected_exit_code
        assert result.output == expected_output

    @pytest.mark.usefixtures('flushall_redis_server')
    def test_device_remove_success(self):
        # setup
        runner = CliRunner()
        result = runner.invoke(cli_main, ['schema', 'add', 'key:int'])
        schema_uuid = result.output.split()[1][1:-1]  # Schema "{uuid}" is added.\n

        device_add_params = ['--name', 'device_name',
                             '--schema', schema_uuid,
                             '--property', 'name:new_device,group:k_dai']
        result = runner.invoke(cli_main, ['device', 'add'] + device_add_params)
        device_uuid = result.output.split()[1][1:-1]  # Device "{uuid}" is added.\n

        # test
        result = runner.invoke(cli_main, ['device', 'remove', device_uuid])
        assert result.exit_code == 0
        assert result.output == 'Device "{}" is removed.\n'.format(device_uuid)

    @pytest.mark.usefixtures('flushall_redis_server')
    @pytest.mark.parametrize(('main_params', 'device_property_params', 'expected_exit_code', 'expected_output'), [
        (['--config', url_scheme_ini_file],  # main_params
         ['--add', 'position:north',
          '--remove', 'type',
          '838c8a6d-4946-4715-ae4b-39d0d64884fb'],  # device_property_params
         -1,  # expected_exit_code
         'Cannot edit INI File.\n'),  # expected_output

        ([],  # main_params
         ['00000000-0000-0000-0000-000000000000'],  # device_property_params
         -1,  # expected_exit_code
         'Device "00000000-0000-0000-0000-000000000000" is not registered. Do nothing.\n'),  # expected_output
    ])
    def test_device_property_failure(self, main_params, device_property_params, expected_exit_code, expected_output):
        runner = CliRunner()
        result = runner.invoke(cli_main, main_params + ['device', 'property'] + device_property_params)
        assert result.exit_code == expected_exit_code
        assert result.output == expected_output

    @pytest.mark.usefixtures('flushall_redis_server')
    @pytest.mark.parametrize(('device_property_params_without_uuid', 'expected_exit_code', 'expected_output'), [
        (['--remove', 'type'],  # device_property_params_without_uuid
         -1,  # expected_exit_code
         'Argument "remove" is invalid : "type" is not exist in properties. Do nothing.\n'),  # expected_output

        (['--add', 'endtime=201203231800'],  # device_property_params_without_uuid
         -1,  # expected_exit_code
         'Argument "add" is invalid : endtime=201203231800. Do nothing.\n'
         'Argument "add" format must be "name1:type1,name2:type2...".\n'),  # expected_output
    ])
    def test_device_property_failure_invalid_argument(self,
                                                      device_property_params_without_uuid,
                                                      expected_exit_code,
                                                      expected_output):
        # setup
        runner = CliRunner()
        result = runner.invoke(cli_main, ['schema', 'add', 'key:int'])
        schema_uuid = result.output.split()[1][1:-1]  # Schema "{uuid}" is added.\n

        device_add_params = ['--name', 'device_name',
                             '--schema', schema_uuid,
                             '--property', 'name:new_device,group:k_dai']
        result = runner.invoke(cli_main, ['device', 'add'] + device_add_params)
        device_uuid = result.output.split()[1][1:-1]  # Device "{uuid}" is added.\n

        # test
        device_property_params = device_property_params_without_uuid + [device_uuid]
        result = runner.invoke(cli_main, ['device', 'property'] + device_property_params)
        assert result.exit_code == expected_exit_code
        assert result.output == expected_output

    @pytest.mark.usefixtures('flushall_redis_server')
    def test_device_property_success(self):
        # setup
        runner = CliRunner()
        result = runner.invoke(cli_main, ['schema', 'add', 'key:int'])
        schema_uuid = result.output.split()[1][1:-1]  # Schema "{uuid}" is added.\n

        device_add_params = ['--name', 'device_name',
                             '--schema', schema_uuid,
                             '--property', 'name:new_device,group:k_dai']
        result = runner.invoke(cli_main, ['device', 'add'] + device_add_params)
        device_uuid = result.output.split()[1][1:-1]  # Device "{uuid}" is added.\n

        # test
        device_property_params = ['--add', 'position:south,start_at:20111211',
                                  '--remove', 'group',
                                  device_uuid]
        result = runner.invoke(cli_main, ['device', 'property'] + device_property_params)
        assert result.exit_code == 0
        assert result.output == 'Device "{}" is updated.\n'.format(device_uuid)

        device_property_params = ['--add', 'position:east',
                                  device_uuid]
        result = runner.invoke(cli_main, ['device', 'property'] + device_property_params)
        assert result.exit_code == 0
        assert result.output == 'Device "{}" is updated.\n'.format(device_uuid)
