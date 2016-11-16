#!/usr/bin/env python
# -*- coding: utf-8 -*-

# community module
import click

# project module
from ..models import Config


@click.group()
@click.option('config_url', '--config', envvar='CRCR_CONFIG')
@click.option('crcr_uuid', '--uuid', envvar='CRCR_UUID')
@click.pass_context
def cli_main(ctx, config_url, crcr_uuid):
    # type: (Any, str, str) -> None
    ctx.obj = {
        'config_url': config_url,
        'config': Config.parse(config_url),
        'uuid': crcr_uuid,
    }


@cli_main.command('env')
@click.pass_context
def cli_main_env(ctx):
    # type: (Any) -> None
    click.echo(ctx.obj['config_url'])
    click.echo(ctx.obj['uuid'])
