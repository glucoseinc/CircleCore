# -*- coding: utf-8 -*-

"""CLI Module."""

# system module
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
    from typing import List, Optional, Tuple


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
    header = ['UUID', 'DISPLAY_NAME', 'TAGS']
    data = []  # type: List[List[str]]
    for module in modules:
        display_name = module.display_name or ''
        data.append([
            str(module.uuid),
            display_name,
            module.stringified_tags,
        ])
    return data, header


@cli_module.command('detail')
@click.argument('module_uuid', type=UUID)
@click.pass_context
def module_detail(ctx, module_uuid):
    """モジュールの詳細を表示する.

    :param Context ctx: Context
    :param UUID module_uuid: モジュールUUID
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
    ]

    for i, message_box_uuid in enumerate(module.message_box_uuids):
        data.append(('MESSAGE_BOX_UUID' if i == 0 else '', str(message_box_uuid)))

    for i, tag in enumerate(module.tags):
        data.append(('TAG' if i == 0 else '', tag))

    data.append(('MEMO', module.memo or ''))

    output_properties(data)

    for message_box_uuid in module.message_box_uuids:
        click.echo('-' * 32)
        message_box = metadata.find_message_box(message_box_uuid)
        data = [
            ('UUID', str(message_box.uuid)),
            ('DISPLAY_NAME', message_box.display_name or ''),
            ('SCHEMA_UUID', str(message_box.schema_uuid)),
            ('MEMO', message_box.memo or ''),
        ]
        output_properties(data)


@cli_module.command('add')
@click.option('display_name', '--name')
@click.option('stringified_message_box_uuids', '--box', required=True)
@click.option('tags', '--tag')
@click.option('--memo')
@click.pass_context
def module_add(ctx, display_name, stringified_message_box_uuids, tags, memo):
    """モジュールを登録する.

    :param Context ctx: Context
    :param Optional[str] display_name: モジュール表示名
    :param str stringified_message_box_uuids: メッセージボックスUUIDリスト(文字列化)
    :param Optional[str] tags: タグ
    :param Optional[str] memo: メモ
    """
    context_object = ctx.obj  # type: ContextObject
    metadata = context_object.metadata

    if not metadata.writable:
        click.echo('Cannot register to {}.'.format(metadata.stringified_type))
        ctx.exit(code=-1)

    module_uuid = generate_uuid(existing=[module.uuid for module in metadata.modules])

    message_boxes = []
    message_box_uuids = stringified_message_box_uuids.split(',')
    for message_box_uuid in message_box_uuids:
        message_box = metadata.find_message_box(message_box_uuid)
        if message_box is None:
            click.echo('MessageBox "{}" is not exist. Do nothing.'.format(message_box_uuid))
            ctx.exit(code=-1)
        message_boxes.append(message_box)

    module = Module(
        module_uuid,
        message_box_uuids,
        display_name,
        tags,
        memo
    )

    metadata.register_module(module)
    context_object.log_info('module add', uuid=module.uuid)
    click.echo('Module "{}" is added.'.format(module.uuid))


@cli_module.command('remove')
@click.argument('module_uuid', type=UUID)
@click.pass_context
def module_remove(ctx, module_uuid):
    """モジュールを削除する.

    :param Context ctx: Context
    :param UUID module_uuid: モジュールUUID
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
