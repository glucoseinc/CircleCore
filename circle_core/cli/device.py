#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""CLI Device."""

# system module
from uuid import uuid4

# community module
import click
from click.core import Context
from six import PY3

# project module
from .context import ContextObject
from .utils import output_listing_columns, output_properties
from ..models import Device
from ..models.config import ConfigRedis

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
    header = ['UUID', 'DISPLAY_NAME', 'SCHEMA_UUID', 'PROPERTIES']
    data = []  # type: List[List[str]]
    for device in devices:
        display_name = device.display_name or ''
        data.append([device.uuid, display_name, device.schema_uuid, device.stringified_properties])
    return data, header


@cli_device.command('detail')
@click.argument('device_uuid')
@click.pass_context
def schema_detail(ctx, device_uuid):
    """デバイスの詳細を表示する.

    :param Context ctx: Context
    :param str device_uuid: デバイスUUID
    """
    context_object = ctx.obj  # type: ContextObject
    config = context_object.config

    device = config.matched_device(device_uuid)
    if device is None:
        click.echo('Device "{}" is not registered.'.format(device_uuid))
        ctx.exit(code=-1)

    data = [
        ('UUID', device.uuid),
        ('DISPLAY_NAME', device.display_name or ''),
        ('SCHEMA_UUID', device.schema_uuid),
    ]
    for i, prop in enumerate(device.properties):
        data.append(('PROPERTIES' if i == 0 else '', '{}:{}'.format(prop.name, prop.value)))

    output_properties(data)

    # TODO: Schema情報を表示


@cli_device.command('add')
@click.option('display_name', '--name')
@click.option('schema_uuid', '--schema')
@click.option('properties_string', '--property')
@click.option('--active/--inactive')
@click.pass_context
def device_add(ctx, display_name, schema_uuid, properties_string, active):
    """デバイスを登録する.

    :param Context ctx: Context
    :param str display_name: デバイス表示名
    :param str schema_uuid: スキーマUUID
    :param str properties_string: プロパティ
    :param bool active:
    """
    context_object = ctx.obj  # type: ContextObject
    config = context_object.config

    if not isinstance(config, (ConfigRedis,)):
        click.echo('Cannot register to {}.'.format(config.stringified_type))
        ctx.exit(code=-1)

    device_uuid = str(uuid4())
    # TODO: 重複チェックする

    schema = config.matched_schema(schema_uuid)
    if schema is None:
        click.echo('Schema "{}" is not exist.'.format(schema_uuid))
        ctx.exit(code=-1)

    properties = {}
    for i, string in enumerate(properties_string.split(','), start=1):
        splitted = [val.strip() for val in string.split(':')]
        if len(splitted) != 2:
            click.echo('Argument "property" is invalid : {}.'.format(string))
            ctx.exit(code=-1)
        _property, _value = splitted[0], splitted[1]
        properties['property{}'.format(i)] = _property
        properties['value{}'.format(i)] = _value

    device = Device(device_uuid, schema.uuid, display_name, **properties)
    # TODO: activeの扱い

    if isinstance(config, ConfigRedis):
        redis_client = config.redis_client
        if redis_client is None:
            click.echo('Cannot connect to Redis server.')
            ctx.exit(code=-1)

        device.register_to_redis(redis_client)
        click.echo('Device "{}" is added.'.format(device.uuid))


@cli_device.command('remove')
@click.argument('device_uuid')
@click.pass_context
def device_remove(ctx, device_uuid):
    """デバイスを削除する.

    :param Context ctx: Context
    :param str device_uuid: デバイスUUID
    """
    context_object = ctx.obj  # type: ContextObject
    config = context_object.config

    if not isinstance(config, (ConfigRedis,)):
        click.echo('Cannot remove from {}.'.format(config.stringified_type))
        ctx.exit(code=-1)

    if isinstance(config, ConfigRedis):
        redis_client = config.redis_client
        device = config.matched_device(device_uuid)
        if device is None:
            click.echo('Device "{}" is not registered. Do nothing.'.format(device_uuid))
            ctx.exit(code=-1)
        device.unregister_from_redis(redis_client)
        click.echo('Device "{}" is removed.'.format(device_uuid))


@cli_device.command('property')
@click.option('adding_properties_string', '--add')
@click.option('removing_property_names_string', '--remove')
@click.argument('device_uuid')
@click.pass_context
def device_property(ctx, adding_properties_string, removing_property_names_string, device_uuid):
    """デバイスのプロパティを更新する.

    :param Context ctx: Context
    :param str adding_properties_string: 追加プロパティ
    :param str removing_property_names_string: 削除プロパティ
    :param str device_uuid: デバイスUUID
    """
    context_object = ctx.obj  # type: ContextObject
    config = context_object.config

    if not isinstance(config, (ConfigRedis,)):
        click.echo('Cannot edit {}.'.format(config.stringified_type))
        ctx.exit(code=-1)

    if isinstance(config, ConfigRedis):
        redis_client = config.redis_client
        device = config.matched_device(device_uuid)
        if device is None:
            click.echo('Device "{}" is not registered. Do nothing.'.format(device_uuid))
            ctx.exit(code=-1)
        if removing_property_names_string is not None:
            removing_property_names = set([key.strip() for key in removing_property_names_string.split(',')])
            current_property_names = set([prop.name for prop in device.properties])
            if not removing_property_names.issubset(current_property_names):
                difference_property_names = removing_property_names.difference(current_property_names)
                click.echo('Argument "remove" is invalid : "{}" is not exist in properties. Do nothing.'
                           .format(','.join(difference_property_names)))
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
        click.echo('Device "{}" is updated.'.format(device_uuid))
