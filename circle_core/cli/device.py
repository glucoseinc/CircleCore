#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""CLI Device."""

# community module
import click
from click.core import Context
from six import PY3

# project module
from .context import ContextObject
from .utils import output_listing_columns, output_properties
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


@cli_device.command('detail')
@click.argument('device_name')
@click.pass_context
def schema_detail(ctx, device_name):
    """デバイスの詳細を表示する.

    :param Context ctx: Context
    :param str device_name: デバイス表示名
    """
    context_object = ctx.obj  # type: ContextObject
    config = context_object.config

    device = config.matched_device(device_name)
    if device is None:
        click.echo('Device "{}" is not registered.'.format(device_name))
        ctx.exit(code=-1)

    data = [
        ('DISPLAY_NAME', device.display_name),
        ('SCHEMA', device.schema_uuid),
    ]
    for i, prop in enumerate(device.properties):
        data.append(('PROPERTIES' if i == 0 else '', '{}:{}'.format(prop.name, prop.value)))

    output_properties(data)

    # TODO: Schema情報を表示


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
    :param str group:
    :param str properties_string: プロパティ
    :param bool active:
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
    # TODO: groupとactiveの扱いW

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


@cli_device.command('remove')
@click.argument('device_name')
@click.pass_context
def device_remove(ctx, device_name):
    """デバイスを削除する.

    :param Context ctx: Context
    :param str device_name: デバイス表示名
    """
    context_object = ctx.obj  # type: ContextObject
    config = context_object.config

    if config.type not in (ConfigType.redis,):
        click.echo('Cannot remove from {}.'.format(config.stringified_type))
        ctx.exit(code=-1)

    if config.type == ConfigType.redis:
        redis_client = config.redis_client
        device = config.matched_device(device_name)
        if device is None:
            click.echo('Device "{}" is not registered. Do nothing.'.format(device_name))
            ctx.exit(code=-1)
        device.unregister_from_redis(redis_client)
        click.echo('Device "{}" is removed.'.format(device_name))


@cli_device.command('property')
@click.option('adding_properties_string', '--add')
@click.option('removing_property_names_string', '--remove')
@click.argument('device_name')
@click.pass_context
def device_property(ctx, adding_properties_string, removing_property_names_string, device_name):
    """デバイスのプロパティを更新する.

    :param Context ctx: Context
    :param str adding_properties_string: 追加プロパティ
    :param str removing_property_names_string: 削除プロパティ
    :param str device_name: デバイス表示名
    """
    context_object = ctx.obj  # type: ContextObject
    config = context_object.config

    if config.type not in (ConfigType.redis,):
        click.echo('Cannot edit {}.'.format(config.stringified_type))
        ctx.exit(code=-1)

    if config.type == ConfigType.redis:
        redis_client = config.redis_client
        device = config.matched_device(device_name)
        if device is None:
            click.echo('Device "{}" is not registered. Do nothing.'.format(device_name))
            ctx.exit(code=-1)
        if removing_property_names_string is not None:
            removing_property_names = set([key.strip() for key in removing_property_names_string.split(',')])
            current_property_names = set([prop.name for prop in device.properties])
            if not removing_property_names.issubset(current_property_names):
                difference_property_names = removing_property_names.difference(current_property_names)
                click.echo('Argument "remove" is invalid : "{}" is not exist in "{}"\'s properties. Do nothing.'
                           .format(','.join(difference_property_names), device_name))
                ctx.exit(code=-1)
            device.remove_properties(list(removing_property_names))

        if adding_properties_string is not None:
            adding_properties = []
            for i, string in enumerate(adding_properties_string.split(','), start=1):
                splitted = [val.strip() for val in string.split(':')]
                if len(splitted) != 2:
                    click.echo('Argument "add" is invalid : {}.'.format(string))
                    ctx.exit(code=-1)
                name, value = splitted[0], splitted[1]
                adding_properties.append((name, value))
            device.append_properties(adding_properties)

        device.update_in_redis(redis_client)
        click.echo('Device "{}" is updated.'.format(device_name))
