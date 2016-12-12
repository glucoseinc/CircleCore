# -*- coding: utf-8 -*-

"""CLI Module."""

from uuid import UUID

# community module
import click
from click.core import Context
from six import PY3

# project module
from .context import ContextObject
from .utils import generate_uuid, output_listing_columns, output_properties
from ..models import Module

if PY3:
    from typing import List, Tuple


@click.group('module')
def cli_module():
    """`crcr module`の起点."""
    pass


@cli_module.command('list')
@click.pass_context
def module_list(ctx):
    """登録中のモジュール一覧を表示する.

    :param Context ctx: Context
    """
    context_object = ctx.obj  # type: ContextObject
    metadata = context_object.metadata
    modules = metadata.modules
    if len(modules):
        data, header = _format_for_columns(modules)
        output_listing_columns(data, header)
    else:
        click.echo('No modules are registered.')


def _format_for_columns(modules):
    """モジュールリストを表示用に加工する.

    :param List[Module] modules: モジュールリスト
    :return: data: 加工後のモジュールリスト, header: 見出し
    :rtype: Tuple[List[List[str]], List[str]]
    """
    header = ['UUID', 'DISPLAY_NAME', 'SCHEMA_UUID', 'PROPERTIES']
    data = []  # type: List[List[str]]
    for module in modules:
        display_name = module.display_name or ''
        data.append([str(module.uuid), display_name, str(module.schema_uuid), module.stringified_properties])
    return data, header


@cli_module.command('detail')
@click.argument('module_uuid', type=UUID)
@click.pass_context
def module_detail(ctx, module_uuid):
    """モジュールの詳細を表示する.

    :param Context ctx: Context
    :param str module_uuid: モジュールUUID
    """
    context_object = ctx.obj  # type: ContextObject
    metadata = context_object.metadata

    module = metadata.find_module(module_uuid)
    if module is None:
        click.echo('Module "{}" is not registered.'.format(module_uuid))
        ctx.exit(code=-1)

    data = [
        ('UUID', str(module.uuid)),
        ('DISPLAY_NAME', module.display_name or ''),
        ('SCHEMA_UUID', str(module.schema_uuid)),
    ]
    for i, prop in enumerate(module.properties):
        data.append(('PROPERTIES' if i == 0 else '', '{}:{}'.format(prop.name, prop.value)))

    output_properties(data)

    # TODO: Schema情報を表示


@cli_module.command('add')
@click.option('display_name', '--name')
@click.option('schema_uuid', '--schema', type=UUID)
@click.option('properties', '--property')
@click.option('--active/--inactive')
@click.pass_context
def module_add(ctx, display_name, schema_uuid, properties, active):
    """モジュールを登録する.

    :param Context ctx: Context
    :param str display_name: モジュール表示名
    :param str schema_uuid: スキーマUUID
    :param str properties: プロパティ
    :param bool active:
    """
    context_object = ctx.obj  # type: ContextObject
    metadata = context_object.metadata

    if not metadata.writable:
        click.echo('Cannot register to {}.'.format(metadata.stringified_type))
        ctx.exit(code=-1)

    module_uuid = generate_uuid(existing=[module.uuid for module in metadata.modules])

    schema = metadata.find_schema(schema_uuid)
    if schema is None:
        click.echo('Schema "{}" is not exist. Do nothing.'.format(schema_uuid))
        ctx.exit(code=-1)

    for prop in properties.split(','):
        splitted = [val.strip() for val in prop.split(':')]
        if len(splitted) != 2:
            click.echo('Argument "property" is invalid : {}. Do nothing.'.format(prop))
            click.echo('Argument "property" format must be "name1:type1,name2:type2...".')
            ctx.exit(code=-1)

    module = Module(module_uuid, schema.uuid, display_name, properties)
    # TODO: activeの扱い

    metadata.register_module(module)
    context_object.log_info('module add', uuid=module.uuid)
    click.echo('Module "{}" is added.'.format(module.uuid))


@cli_module.command('remove')
@click.argument('module_uuid', type=UUID)
@click.pass_context
def module_remove(ctx, module_uuid):
    """モジュールを削除する.

    :param Context ctx: Context
    :param str module_uuid: モジュールUUID
    """
    context_object = ctx.obj  # type: ContextObject
    metadata = context_object.metadata

    if not metadata.writable:
        click.echo('Cannot remove from {}.'.format(metadata.stringified_type))
        ctx.exit(code=-1)

    module = metadata.find_module(module_uuid)
    if module is None:
        click.echo('Module "{}" is not registered. Do nothing.'.format(module_uuid))
        ctx.exit(code=-1)
    metadata.unregister_module(module)
    context_object.log_info('module remove', uuid=module_uuid)
    click.echo('Module "{}" is removed.'.format(module_uuid))


@cli_module.command('property')
@click.option('adding_properties_string', '--add')
@click.option('removing_property_names_string', '--remove')
@click.argument('module_uuid', type=UUID)
@click.pass_context
def module_property(ctx, adding_properties_string, removing_property_names_string, module_uuid):
    """モジュールのプロパティを更新する.

    :param Context ctx: Context
    :param str adding_properties_string: 追加プロパティ
    :param str removing_property_names_string: 削除プロパティ
    :param str module_uuid: モジュールUUID
    """
    context_object = ctx.obj  # type: ContextObject
    metadata = context_object.metadata

    if not metadata.writable:
        click.echo('Cannot edit {}.'.format(metadata.stringified_type))
        ctx.exit(code=-1)

    module = metadata.find_module(module_uuid)
    if module is None:
        click.echo('Module "{}" is not registered. Do nothing.'.format(module_uuid))
        ctx.exit(code=-1)
    if removing_property_names_string is not None:
        removing_property_names = set([key.strip() for key in removing_property_names_string.split(',')])
        current_property_names = set([prop.name for prop in module.properties])
        if not removing_property_names.issubset(current_property_names):
            difference_property_names = removing_property_names.difference(current_property_names)
            click.echo('Argument "remove" is invalid : "{}" is not exist in properties. Do nothing.'
                       .format(','.join(difference_property_names)))
            ctx.exit(code=-1)
        module.remove_properties(list(removing_property_names))

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
        module.append_properties(adding_properties)

    metadata.update_module(module)
    context_object.log_info('module update', uuid=module_uuid)
    click.echo('Module "{}" is updated.'.format(module_uuid))
