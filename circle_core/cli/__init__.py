#!/usr/bin/env python
# -*- coding: utf-8 -*-

import click


@click.group()
@click.option('--config', envvar='CRCR_CONFIG')
@click.option('crcr_uuid', '--uuid', envvar='CRCR_UUID')
@click.pass_context
def cli_main(ctx, config, crcr_uuid):
    ctx.obj = {
        'config': config,
        'uuid': crcr_uuid,
    }


@cli_main.command('env')
@click.pass_context
def cli_env(ctx):
    click.echo(ctx.obj['config'])
    click.echo(ctx.obj['uuid'])
