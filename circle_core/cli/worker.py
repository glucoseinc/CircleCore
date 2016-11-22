#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""CLI Worker."""
from importlib import import_module

import click


@click.group('worker')
def cli_worker():
    """`crcr worker`の起点."""
    pass


@cli_worker.command()
def list():
    """ワーカー一覧."""
    raise NotImplementedError


@cli_worker.command()
@click.argument('name')
def run(name):
    """ワーカーの起動.

    :param str name: ワーカーのファイル名.
    """
    try:
        worker = import_module('circle_core.workers.{}'.format(name))
    except ImportError:
        click.echo('The worker is not found', err=True)
    else:
        click.echo('The worker is waiting for messages')
        worker.run()
