# -*- coding: utf-8 -*-
"""CircleCore CLI."""

import importlib

# project module
from .cli_main import cli_main as cli_entry

for key in (
    'box', 'invitation', 'module', 'replication_link', 'replication_master', 'schema', 'user', 'cliutil', 'debug'
):
    mod = importlib.import_module('.{}'.format(key), __name__)
    group = getattr(mod, 'cli_{}'.format(key))
    cli_entry.add_command(group)
