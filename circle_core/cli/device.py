#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""CLI Device."""

# community module
import click
from click.core import Context
from six import PY3

# project module
from .context import ContextObject
from .utils import output_listing_columns
from ..models import Device

if PY3:
    from typing import List, Tuple


@click.group('device')
@click.pass_context
def cli_device(ctx):
    """`crcr device`の起点.

    :param Context ctx: Context
    """
    pass


@cli_device.command('list')
@click.pass_context
def device_list(ctx):
    """登録中のデバイス一覧を表示する.

    :param Context ctx: Context
    """
    context_object = ctx.obj  # type: ContextObject
    config = context_object.config
    devices = config.devices
    if len(devices):
        data, header = _format_for_columns(devices)
        output_listing_columns(data, header)
    else:
        click.echo('No devices are registered.')


def _format_for_columns(devices):
    """デバイスリストを表示用に加工する.

    :param List[Device] devices: デバイスリスト
    :return: data: 加工後のデバイスリスト, header: 見出し
    :rtype: Tuple[List[List[str]], List[str]]
    """
    header = ['SCHEMA', 'DISPLAY_NAME', 'PROPERTIES']
    data = [[device.schema_uuid, device.display_name, device.stringified_properties]
            for device in devices]
    return data, header
