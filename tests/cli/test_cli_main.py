# -*- coding: utf-8 -*-

# system module
from collections import defaultdict
import os

# community module
from click.testing import CliRunner
import pytest

# project module
from circle_core.cli import cli_entry
from tests import crcr_uuid


@pytest.mark.skip
class TestCliMain(object):
    @pytest.mark.usefixtures('remove_environ')
    @pytest.mark.parametrize(('main_params', 'expected'), [
        (
            [],  # main_params
            {'exit_code': -1,
             'output': ['Metadata is not set.',
                        'Please set metadata to argument `crcr --metadata URL_SCHEME ...`',
                        'or set to environment variable `export CRCR_METADATA=URL_SCHEME`.']},  # expected
        ),
        (
            ['--metadata', 'redis://localhost:65535/16'],  # main_params
            {'exit_code': -1,
             'output': ['Invalid metadata url / '
                        'Cannot connect to Redis server. : redis://localhost:65535/16']},  # expected
        ),
    ])
    def test_main_env_failure(self, main_params, expected):
        runner = CliRunner()
        result = runner.invoke(cli_entry, main_params + ['env'])
        assert result.exit_code == expected['exit_code']
        assert result.output == '\n'.join(expected['output']) + '\n'

    @pytest.mark.parametrize(('main_param_uuid', 'expected'), [
        (['--log-file', '/tmp/log.ltsv'],  # main_param_uuid
         {'output_uuid': crcr_uuid,
          'output_log_file_path': '/tmp/log.ltsv'}),  # expected
    ])
    def test_main_env_success(self, main_param_uuid, expected):
        # from circle_core.cli import cli_entry

        metadata = os.environ['CRCR_METADATA']
        main_params = ['--metadata', metadata] + main_param_uuid
        runner = CliRunner()
        result = runner.invoke(cli_entry, main_params + ['env'])
        assert result.exit_code == 0
        assert result.output == '\n'.join([metadata,
                                           expected['output_uuid'],
                                           expected['output_log_file_path']]) + '\n'

    def test_main_migrate_failure(self, monkeypatch):
        """`--database`オプションなしでmigrateを呼んだらエラーにする"""
        default_args = [
            '--metadata', 'file:///{}/tests/metadata.ini'.format(os.getcwd()),
            'migrate'
        ]
        result = CliRunner().invoke(cli_entry, default_args)
        assert result.exit_code != 0

    @pytest.mark.skip
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
            '--metadata', 'file:///{}/tests/metadata.ini'.format(os.getcwd()),
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
