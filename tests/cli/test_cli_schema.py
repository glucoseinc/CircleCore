#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from circle_core.cli import cli_main
from click.testing import CliRunner
import pytest
import redis
import tcptest.redis

from tests import test_root


@pytest.fixture(autouse=True, scope='module')
def redis_server(request):
    server = tcptest.redis.Server()
    server.start()

    def stop():
        server.stop()
    request.addfinalizer(stop)
    return server


@pytest.fixture()
def flushall_redis_server(redis_server):
    redis.Redis(port=redis_server.port).flushall()


class TestCliSchema(object):
    @pytest.mark.parametrize(('main_params', 'expected_output_length'), [
        (['--config', 'file://{}'.format(os.path.join(test_root, 'config.ini'))],  # main_params
         4),  # expected_output_length
    ])
    def test_schema_list(self, main_params, expected_output_length):
        runner = CliRunner()
        result = runner.invoke(cli_main, main_params + ['schema', 'list'])
        assert result.exit_code == 0
        len(result.output.split('\n')) == expected_output_length

    @pytest.mark.parametrize(('main_params', 'schema_add_params', 'expected'), [
        (['--config', 'file://{}'.format(os.path.join(test_root, 'config.ini'))],  # main_params
         ['schema_name', 'key:int'],  # schema_add_params
         {'exit_code': -1, 'output': 'Cannot register to INI File.\n'}),  # expected

        (['--config', 'redis://localhost:65535/16'],  # main_params
         ['schema_name', 'key:int'],  # schema_add_params
         {'exit_code': -1, 'output': 'Cannot connect to Redis server.\n'}),  # expected

    ])
    def test_schema_add_failure(self, main_params, schema_add_params, expected):
        runner = CliRunner()
        result = runner.invoke(cli_main, main_params + ['schema', 'add'] + schema_add_params)
        assert result.exit_code == expected['exit_code']
        assert result.output == expected['output']

    @pytest.mark.usefixtures('flushall_redis_server')
    @pytest.mark.parametrize(('schema_add_params', 'expected'), [
        (['schema_name', 'key:int'],  # schema_add_params
         {'exit_code': 0, 'output': 'Added.\n'}),  # expected
    ])
    def test_schema_add_success(self, schema_add_params, expected, redis_server, flushall_redis_server):
        config = 'redis://localhost:{}/0'.format(redis_server.port)
        main_params = ['--config', config]

        runner = CliRunner()
        result = runner.invoke(cli_main, main_params + ['schema', 'add'] + schema_add_params)
        assert result.exit_code == expected['exit_code']
        assert result.output == expected['output']
