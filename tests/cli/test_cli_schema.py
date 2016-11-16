#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from circle_core.cli import cli_main
from click.testing import CliRunner
import pytest

from tests import test_root


class TestCliDevice(object):
    @pytest.mark.parametrize(('main_params', 'expected_output_length'), [
        (['--config', 'file://{}'.format(os.path.join(test_root, 'config.ini'))],  # main_params
         4),  # expected_output_length
    ])
    def test_device_list(self, main_params, expected_output_length):
        runner = CliRunner()
        result = runner.invoke(cli_main, main_params + ['schema', 'list'])
        assert result.exit_code == 0
        len(result.output.split('\n')) == expected_output_length
