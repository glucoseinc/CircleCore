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
def run():
    """サーバーの起動."""
    click.echo('Tornado and Flask are running')
    server.run()
