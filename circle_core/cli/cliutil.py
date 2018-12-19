# -*- coding: utf-8 -*-
"""CLI utility commands."""

# system module
import time
from uuid import UUID

# community module
from base58 import b58decode

import click

from dateutil import parser


@click.group('util')
def cli_util():
    """`crcr util`の起点."""
    pass


@cli_util.command('hex2uuid')
@click.argument('hex')
@click.pass_context
def hex2uuid(ctx: 'click.Context', hex: str) -> None:
    """base58表現をUUIDに変換する

    Args:
        ctx: click's Context
    """
    uuid = UUID(bytes=b58decode(hex))
    click.echo('{}'.format(uuid))


@cli_util.command('date2ts')
@click.argument('date')
@click.pass_context
def date2ts(ctx: 'click.Context', date: str) -> None:
    """日付をunix timestampにする

    Args:
        ctx: click's Context
    """
    ts = time.mktime(parser.parse(date).timetuple())
    click.echo('{}'.format(ts))


@cli_util.command()
@click.argument('ts', type=int)
@click.pass_context
def ts2date(ctx: 'click.Context', ts: int) -> None:
    """unix timestampを日付する

    Args:
        ctx: click's Context
    """
    click.echo('UTC:   {}'.format(time.gmtime(ts)))
    click.echo('Local: {}'.format(time.localtime(ts)))


cli_cliutil = cli_util
