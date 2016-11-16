#!/usr/bin/env python
# -*- coding: utf-8 -*-

from circle_core.cli import cli_main
from click.testing import CliRunner
import pytest


class TestCliMain(object):
    @pytest.mark.parametrize(('main_params', 'expected_output'), [
        ([],  # main_params
         ['redis://localhost:5963/1',
          '12345678-9abc-def0-1234-56789abcdef0']),  # expected_output
        (['--config', 'redis://localhost:4771/5',
          '--uuid', '11111111-2222-3333-4444-555555555555'],  # main_params
         ['redis://localhost:4771/5',
          '11111111-2222-3333-4444-555555555555']),  # expected_output
    ])
    def test_main_env(self, main_params, expected_output):
        runner = CliRunner()
        result = runner.invoke(cli_main, main_params + ['env'])
        assert result.exit_code == 0
        assert result.output == '\n'.join(expected_output) + '\n'
