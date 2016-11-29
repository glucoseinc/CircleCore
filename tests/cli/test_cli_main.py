# -*- coding: utf-8 -*-
import os

from click.testing import CliRunner
import pytest

from circle_core.cli import cli_main


class TestCliMain(object):
    @pytest.mark.usefixtures('remove_environ')
    @pytest.mark.parametrize(('main_params', 'expected'), [
        (
            [],  # main_params
            {'exit_code': -1,
             'output': ['Config is not set.',
                        'Please set config to argument `crcr --config URL_SCHEME ...`',
                        'or set config to environment variable `export CRCR_CONFIG=URL_SCHEME`.']},  # expected
        ),
        (
            ['--config', 'redis://localhost:6379/1'],  # main_params
            {'exit_code': -1,
             'output': ['Circle Core UUID is not set.',
                        'Please set UUID to argument `crcr --uuid UUID ...`',
                        'or set config to environment variable `export CRCR_UUID=UUID`.']},  # expected
        ),
        (
            ['--config', 'redis://localhost:65535/16',
             '--uuid', '12121212-3434-5656-7878-909090909090'],  # main_params
            {'exit_code': -1,
             'output': ['Invalid config url / '
                        'Cannot connect to Redis server. : redis://localhost:65535/16']},  # expected
        ),
    ])
    def test_main_env_failure(self, main_params, expected):
        runner = CliRunner()
        result = runner.invoke(cli_main, main_params + ['env'])
        assert result.exit_code == expected['exit_code']
        assert result.output == '\n'.join(expected['output']) + '\n'

    @pytest.mark.parametrize(('main_param_uuid', 'expected'), [
        (['--uuid', '12121212-3434-5656-7878-909090909090'],  # main_param_uuid
         {'output_uuid': '12121212-3434-5656-7878-909090909090'}),  # expected
    ])
    def test_main_env_success(self, main_param_uuid, expected):
        config = os.environ['CRCR_CONFIG']
        main_params = ['--config', config] + main_param_uuid
        runner = CliRunner()
        result = runner.invoke(cli_main, main_params + ['env'])
        assert result.exit_code == 0
        assert result.output == '\n'.join([config, expected['output_uuid']]) + '\n'
