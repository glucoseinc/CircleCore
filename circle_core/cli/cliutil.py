# -*- coding: utf-8 -*-

"""CLI invitation."""

# system module
import datetime
from uuid import UUID
import time

# community module
from base58 import b58decode
from dateutil import parser
import click
from six import PY3


if PY3:
    from typing import List, Tuple


@click.group('util')
def cli_util():
    """`crcr util`の起点."""
    pass


@cli_util.command('hex2uuid')
@click.argument('hex')
@click.pass_context
def hex2uuid(ctx, hex):
    """base58表現をUUIDに変換する

    :param Context ctx: Context
    """
    uuid = UUID(bytes=b58decode(hex))
    click.echo('{}'.format(uuid))


@cli_util.command('date2ts')
@click.argument('date')
@click.pass_context
def date2ts(ctx, date):
    """日付をunix timestampにする

    :param Context ctx: Context
    """
    ts = time.mktime(parser.parse(date).timetuple())
    click.echo('{}'.format(ts))


cli_cliutil = cli_util
