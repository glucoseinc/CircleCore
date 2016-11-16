#!/usr/bin/env python
# -*- coding: utf-8 -*-

# community module
import click

# project module
from ..models import Config  # noqa
from .utils import output_listing_columns, stringify_dict


@click.group('device')
@click.pass_context
def cli_device(ctx):
    pass


@cli_device.command('list')
@click.pass_context
def device_list(ctx):
    config = ctx.obj['config']  # type: Config
    devices = config.devices
    if len(devices):
        data, header = _format_for_columns(devices)
        output_listing_columns(data, header)
    else:
        click.echo('No devices are registered.')


def _format_for_columns(devices):
    header = ['SCHEMA', 'DISPLAY_NAME', 'PROPERTIES']
    data = [[device.schema_uuid, device.display_name, stringify_dict(device.properties)]
            for device in devices]
    return data, header
