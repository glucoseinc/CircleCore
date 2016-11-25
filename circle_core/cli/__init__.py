#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""CircleCore CLI."""

import click
# project module
from .cli_main import cli_main
from .device import cli_device
from .schema import cli_schema
from .server import cli_server
from .worker import cli_worker

cli_main.add_command(cli_device)
cli_main.add_command(cli_schema)
cli_main.add_command(cli_server)
cli_main.add_command(cli_worker)
