#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""CLI Server."""
# community module
import click

# project module
from .context import ContextObject
from ..server import run


@click.group('server')
def cli_server():
    """`crcr server`の起点."""
    pass


@cli_server.command('run')
@click.option('--port', type=click.INT, default=5000)
@click.pass_context
def server_run(ctx, port):
    """サーバーの起動."""
    context_object = ctx.obj  # type: ContextObject
    config = context_object.config

    click.echo('Tornado and Flask are running')
    run(port, config)
