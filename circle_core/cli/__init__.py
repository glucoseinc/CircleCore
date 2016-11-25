# -*- coding: utf-8 -*-

"""CircleCore CLI."""

# project module
from .cli_main import cli_main
from .device import cli_device
from .schema import cli_schema

cli_main.add_command(cli_device)
cli_main.add_command(cli_schema)
