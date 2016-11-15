#!/usr/bin/env python
# -*- coding: utf-8 -*-

from circle_core.cli import cli_main
from click.testing import CliRunner


def test_env():
    def _test_env(params, expected_output):
        result = runner.invoke(cli_main, params + ['env'])
        assert result.exit_code == 0
        assert result.output == '\n'.join(expected_output) + '\n'

    runner = CliRunner()

    params = []
    expected_output = [
        'redis://localhost:5963/1',
        '12345678-9abc-def0-1234-56789abcdef0'
    ]
    _test_env(params, expected_output)

    params = [
        '--config', 'redis://localhost:4771/5',
        '--uuid', '11111111-2222-3333-4444-555555555555'
    ]
    expected_output = [
        'redis://localhost:4771/5',
        '11111111-2222-3333-4444-555555555555'
    ]
    _test_env(params, expected_output)
