#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""CLI Main."""

# community module
import click
from click.core import Context

# project module
from .context import ContextObject, ContextObjectError


@click.group()
@click.option('config_url', '--config', envvar='CRCR_CONFIG')
@click.option('crcr_uuid', '--uuid', envvar='CRCR_UUID')
@click.pass_context
def cli_main(ctx, config_url, crcr_uuid):
    """`crcr`の起点.

    :param Context ctx: Context
    :param str config_url: ConfigのURLスキーム
    :param str crcr_uuid: CircleCore UUID
    """
    if config_url is None:
        click.echo('Config is not set.')
        click.echo('Please set config to argument `crcr --config URL_SCHEME ...`')
        click.echo('or set config to environment variable `export CRCR_CONFIG=URL_SCHEME`.')
        ctx.exit(code=-1)

    if crcr_uuid is None:
        click.echo('Circle Core UUID is not set.')
        click.echo('Please set UUID to argument `crcr --uuid UUID ...`')
        click.echo('or set config to environment variable `export CRCR_UUID=UUID`.')
        ctx.exit(code=-1)

    try:
        ctx.obj = ContextObject(config_url, crcr_uuid)
    except ContextObjectError as e:
        click.echo(e)
        ctx.exit(code=-1)


@cli_main.command('env')
@click.pass_context
def cli_main_env(ctx):
    """CircleCoreの環境を表示する.

    :param Context ctx: Context
    """
    click.echo(ctx.obj.config_url)
    click.echo(ctx.obj.uuid)
