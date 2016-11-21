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
from ..models.config import ConfigType

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


@cli_device.command('add')
@click.option('schema_name', '--schema')
@click.option('--group')
@click.option('properties_string', '--property')
@click.option('--active/--inactive')
@click.argument('device_name')
@click.pass_context
def device_add(ctx, schema_name, group, properties_string, active, device_name):
    """デバイスを登録する.

    :param Context ctx: Context
    :param str schema_name: スキーマ表示名
    :param group:
    :param properties_string: プロパティ
    :param active:
    :param str device_name: デバイス表示名
    """
    context_object = ctx.obj  # type: ContextObject
    config = context_object.config

    if config.type not in (ConfigType.redis,):
        click.echo('Cannot register to {}.'.format(config.stringified_type))
        ctx.exit(code=-1)

    schemas = [schema for schema in config.schemas if schema.display_name == schema_name]
    if len(schemas) == 0:
        click.echo('Schema "{}" is not exist.'.format(schema_name))
        ctx.exit(code=-1)

    schema = sorted(schemas, key=lambda schema: schema.uuid)[0]

    properties = {}
    for i, string in enumerate(properties_string.split(','), start=1):
        splitted = [val.strip() for val in string.split(':')]
        if len(splitted) != 2:
            click.echo('Argument "property" is invalid : {}.'.format(string))
            ctx.exit(code=-1)
        _property, _value = splitted[0], splitted[1]
        properties['property{}'.format(i)] = _property
        properties['value{}'.format(i)] = _value

    device = Device(schema.uuid, device_name, **properties)

    if config.type == ConfigType.redis:
        redis_client = config.redis_client
        if redis_client is None:
            click.echo('Cannot connect to Redis server.')
            ctx.exit(code=-1)

        # 登録されていない最小の数を取得する
        registered_nums = [_device.db_id for _device in config.devices]
        for num in range(1, len(registered_nums) + 2):
            if num not in registered_nums:
                break
        device.db_id = num
        device.register_to_redis(redis_client)
        click.echo('Device "{}" is added.'.format(device.display_name))
