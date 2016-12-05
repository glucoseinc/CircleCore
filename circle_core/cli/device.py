# -*- coding: utf-8 -*-

"""CLI Device."""

from uuid import UUID

# community module
import click
from click.core import Context
from six import PY3

# project module
from .context import ContextObject
from .utils import generate_uuid, output_listing_columns, output_properties
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
    metadata = context_object.metadata
    devices = metadata.devices
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
        data.append([str(device.uuid), display_name, str(device.schema_uuid), device.stringified_properties])
    return data, header


@cli_device.command('detail')
@click.argument('device_uuid', type=UUID)
@click.pass_context
def device_detail(ctx, device_uuid):
    """デバイスの詳細を表示する.

    :param Context ctx: Context
    :param str device_uuid: デバイスUUID
    """
    context_object = ctx.obj  # type: ContextObject
    metadata = context_object.metadata

    device = metadata.find_device(device_uuid)
    if device is None:
        click.echo('Device "{}" is not registered.'.format(device_uuid))
        ctx.exit(code=-1)

    data = [
        ('UUID', str(device.uuid)),
        ('DISPLAY_NAME', device.display_name or ''),
        ('SCHEMA_UUID', str(device.schema_uuid)),
    ]
    for i, prop in enumerate(device.properties):
        data.append(('PROPERTIES' if i == 0 else '', '{}:{}'.format(prop.name, prop.value)))

    output_properties(data)

    # TODO: Schema情報を表示


@cli_device.command('add')
@click.option('display_name', '--name')
@click.option('schema_uuid', '--schema', type=UUID)
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
    metadata = context_object.metadata

    if not metadata.writable:
        click.echo('Cannot register to {}.'.format(metadata.stringified_type))
        ctx.exit(code=-1)

    device_uuid = generate_uuid(existing=[device.uuid for device in metadata.devices])

    schema = metadata.find_schema(schema_uuid)
    if schema is None:
        click.echo('Schema "{}" is not exist. Do nothing.'.format(schema_uuid))
        ctx.exit(code=-1)

    properties = {}
    for i, string in enumerate(properties_string.split(','), start=1):
        splitted = [val.strip() for val in string.split(':')]
        if len(splitted) != 2:
            click.echo('Argument "property" is invalid : {}. Do nothing.'.format(string))
            click.echo('Argument "property" format must be "name1:type1,name2:type2...".')
            ctx.exit(code=-1)
        _property, _value = splitted[0], splitted[1]
        properties['property{}'.format(i)] = _property
        properties['value{}'.format(i)] = _value

    device = Device(device_uuid, schema.uuid, display_name, **properties)
    # TODO: activeの扱い

    metadata.register_device(device)
    context_object.log_info('device add', uuid=device.uuid)
    click.echo('Device "{}" is added.'.format(device.uuid))


@cli_device.command('remove')
@click.argument('device_uuid', type=UUID)
@click.pass_context
def device_remove(ctx, device_uuid):
    """デバイスを削除する.

    :param Context ctx: Context
    :param str device_uuid: デバイスUUID
    """
    context_object = ctx.obj  # type: ContextObject
    metadata = context_object.metadata

    if not metadata.writable:
        click.echo('Cannot remove from {}.'.format(metadata.stringified_type))
        ctx.exit(code=-1)

    device = metadata.find_device(device_uuid)
    if device is None:
        click.echo('Device "{}" is not registered. Do nothing.'.format(device_uuid))
        ctx.exit(code=-1)
    metadata.unregister_device(device)
    context_object.log_info('device remove', uuid=device_uuid)
    click.echo('Device "{}" is removed.'.format(device_uuid))


@cli_device.command('property')
@click.option('adding_properties_string', '--add')
@click.option('removing_property_names_string', '--remove')
@click.argument('device_uuid', type=UUID)
@click.pass_context
def device_property(ctx, adding_properties_string, removing_property_names_string, device_uuid):
    """デバイスのプロパティを更新する.

    :param Context ctx: Context
    :param str adding_properties_string: 追加プロパティ
    :param str removing_property_names_string: 削除プロパティ
    :param str device_uuid: デバイスUUID
    """
    context_object = ctx.obj  # type: ContextObject
    metadata = context_object.metadata

    if not metadata.writable:
        click.echo('Cannot edit {}.'.format(metadata.stringified_type))
        ctx.exit(code=-1)

    device = metadata.find_device(device_uuid)
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
                click.echo('Argument "add" is invalid : {}. Do nothing.'.format(string))
                click.echo('Argument "add" format must be "name1:type1,name2:type2...".')
                ctx.exit(code=-1)
            name, value = splitted[0], splitted[1]
            adding_properties.append((name, value))
        device.append_properties(adding_properties)

    metadata.update_device(device)
    context_object.log_info('device update', uuid=device_uuid)
    click.echo('Device "{}" is updated.'.format(device_uuid))
