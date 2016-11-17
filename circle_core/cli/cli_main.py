#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""CLI Main."""

# community module
import click
from click.core import Context

# project module
from ..models import Config


@click.group()
@click.option('config_url', '--config', envvar='CRCR_CONFIG')
@click.option('crcr_uuid', '--uuid', envvar='CRCR_UUID')
@click.pass_context
def cli_main(ctx, config_url, crcr_uuid):
    """`crcr`の起点.

    :param Context ctx: Context
    :param str config_url: URLスキーム
    :param str crcr_uuid: CircleCore UUID
    """
    ctx.obj = {
        'config_url': config_url,
        'config': Config.parse(config_url),
        'uuid': crcr_uuid,
    }


@cli_main.command('env')
@click.pass_context
def cli_main_env(ctx):
    """CircleCoreの環境を表示する.

    :param Context ctx: Context
    """
    click.echo(ctx.obj['config_url'])
    click.echo(ctx.obj['uuid'])
