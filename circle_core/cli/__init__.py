#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""CircleCore CLI."""

import click
# project module
from .cli_main import cli_main
from .device import cli_device
from .schema import cli_schema

cli_main.add_command(cli_device)
cli_main.add_command(cli_schema)


@cli_main.command()
@click.pass_context
def run_server(ctx):
    from circle_core.server.main import run
    click.echo('Tornado and Flask are running')
    run()
