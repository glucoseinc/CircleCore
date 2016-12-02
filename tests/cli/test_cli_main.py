# -*- coding: utf-8 -*-
from collections import defaultdict
import os

from click.testing import CliRunner
import pytest

from circle_core.cli import cli_entry


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
        result = runner.invoke(cli_entry, main_params + ['env'])
        assert result.exit_code == expected['exit_code']
        assert result.output == '\n'.join(expected['output']) + '\n'

    @pytest.mark.parametrize(('main_param_uuid', 'expected'), [
        (['--uuid', '12121212-3434-5656-7878-909090909090'],  # main_param_uuid
         {'output_uuid': '12121212-3434-5656-7878-909090909090'}),  # expected
    ])
    def test_main_env_success(self, main_param_uuid, expected):
        # from circle_core.cli import cli_entry

        config = os.environ['CRCR_CONFIG']
        main_params = ['--config', config] + main_param_uuid
        runner = CliRunner()
        result = runner.invoke(cli_entry, main_params + ['env'])
        assert result.exit_code == 0
        assert result.output == '\n'.join([config, expected['output_uuid']]) + '\n'

    def test_main_migrate_failure(self, monkeypatch):
        """`--database`オプションなしでmigrateを呼んだらエラーにする"""
        default_args = [
            '--config', 'file:///{}/tests/config.ini'.format(os.getcwd()),
            '--uuid', '12121212-3434-5656-7878-909090909090',
            'migrate'
        ]
        result = CliRunner().invoke(cli_entry, default_args)
        assert result.exit_code != 0

    def test_main_migrate(self, monkeypatch):
        test_db_url = 'mysql+mysqlconnector://localhsot/testtest'
        # DatabaseクラスにPatchを当てる
        call_result = {
            'db_init_params': [],
            'db_calls': defaultdict(list),
        }

        class MockDatabase(object):
            def __init__(self, *args, **kwargs):
                call_result['db_init_params'].append((args, kwargs))

            def __getattr__(self, key):
                def _f(*args, **kwargs):
                    call_result['db_calls'][key].append((args, kwargs))
                return _f

        import circle_core.cli.cli_main
        monkeypatch.setattr(circle_core.cli.cli_main, 'Database', MockDatabase)

        # dry-runなし
        default_args = [
            '--config', 'file:///{}/tests/config.ini'.format(os.getcwd()),
            '--uuid', '12121212-3434-5656-7878-909090909090',
            'migrate', '--database={}'.format(test_db_url)
        ]
        result = CliRunner().invoke(cli_entry, default_args)
        assert result.exit_code == 0

        # check Database() init args
        assert call_result['db_init_params'][0] == ((test_db_url,), {})
        # check migrate was called
        assert len(call_result['db_calls']['migrate']) == 1

        # dry-runあり
        call_result = {
            'db_init_params': [],
            'db_calls': defaultdict(list),
        }
        result = CliRunner().invoke(cli_entry, default_args + ['--dry-run'])
        assert result.exit_code == 0

        # check Database() init args
        assert call_result['db_init_params'][0] == ((test_db_url,), {})
        # check migrate was not called
        assert 'check_tables' in call_result['db_calls']
        assert 'migrate' not in call_result['db_calls']
