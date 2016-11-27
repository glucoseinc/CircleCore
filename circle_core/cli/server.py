#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""CLI Server."""
from circle_core import server
import click


@click.group('server')
def cli_server():
    """`crcr server`の起点."""
    pass


@cli_server.command()
@click.option('--port', type=click.INT, default=5000)
def run(port):
    """サーバーの起動."""
    click.echo('Tornado and Flask are running')
    server.run(port)
