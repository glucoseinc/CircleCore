# -*- coding: utf-8 -*-

"""CLI Box."""

# system module
from uuid import UUID

# community module
import click
from click.core import Context
from six import PY3

# project module
from .context import ContextObject
from .utils import generate_uuid, output_listing_columns, output_properties
from ..models import MessageBox

if PY3:
    from typing import List, Optional, Tuple


@click.group('box')
def cli_box():
    """`crcr box`の起点."""
    pass


@cli_box.command('list')
@click.pass_context
def box_list(ctx):
    """登録中のメッセージボックス一覧を表示する.

    :param Context ctx: Context
    """
    context_object = ctx.obj  # type: ContextObject
    metadata = context_object.metadata
    message_boxes = metadata.message_boxes
    if len(message_boxes):
        data, header = _format_for_columns(message_boxes)
        output_listing_columns(data, header)
    else:
        click.echo('No message boxes are registered.')


def _format_for_columns(message_boxes):
    """メッセージボックスリストを表示用に加工する.

    :param List[MessageBox] message_boxes: メッセージボックスリスト
    :return: data: 加工後のメッセージボックスリスト, header: 見出し
    :rtype: Tuple[List[List[str]], List[str]]
    """
    header = ['UUID', 'DISPLAY_NAME']
    data = []  # type: List[List[str]]
    for message_box in message_boxes:
        display_name = message_box.display_name or ''
        data.append([
            str(message_box.uuid),
            display_name,
        ])
    return data, header


@cli_box.command('detail')
@click.argument('message_box_uuid', type=UUID)
@click.pass_context
def box_detail(ctx, message_box_uuid):
    """モジュールの詳細を表示する.

    :param Context ctx: Context
    :param UUID message_box_uuid: モジュールUUID
    """
    context_object = ctx.obj  # type: ContextObject
    metadata = context_object.metadata

    message_box = metadata.find_message_box(message_box_uuid)
    if message_box is None:
        click.echo('MessageBox "{}" is not registered.'.format(message_box_uuid))
        ctx.exit(code=-1)

    data = [
        ('UUID', str(message_box.uuid)),
        ('DISPLAY_NAME', message_box.display_name or ''),
        ('SCHEMA_UUID', str(message_box.schema_uuid)),
        ('MEMO', message_box.memo or ''),
    ]

    output_properties(data)


@cli_box.command('add')
@click.option('display_name', '--name')
@click.option('schema_uuid', '--schema', type=UUID, required=True)
@click.option('--memo')
@click.pass_context
def box_add(ctx, display_name, schema_uuid, memo):
    """モジュールを登録する.

    :param Context ctx: Context
    :param Optional[str] display_name: モジュール表示名
    :param UUID schema_uuid: スキーマUUID
    :param str memo: メモ
    """
    context_object = ctx.obj  # type: ContextObject
    metadata = context_object.metadata

    if not metadata.writable:
        click.echo('Cannot register to {}.'.format(metadata.stringified_type))
        ctx.exit(code=-1)

    message_box_uuid = generate_uuid(existing=[message_box.uuid for message_box in metadata.message_boxes])

    schema = metadata.find_schema(schema_uuid)
    if schema is None:
        click.echo('Schema "{}" is not exist. Do nothing.'.format(message_box_uuid))
        ctx.exit(code=-1)

    message_box = MessageBox(
        message_box_uuid,
        schema_uuid,
        display_name,
        memo
    )

    metadata.register_message_box(message_box)
    context_object.log_info('message box add', uuid=message_box.uuid)
    click.echo('MessageBox "{}" is added.'.format(message_box.uuid))


@cli_box.command('remove')
@click.argument('message_box_uuid', type=UUID)
@click.pass_context
def box_remove(ctx, message_box_uuid):
    """モジュールを削除する.

    :param Context ctx: Context
    :param UUID message_box_uuid: モジュールUUID
    """
    context_object = ctx.obj  # type: ContextObject
    metadata = context_object.metadata

    if not metadata.writable:
        click.echo('Cannot remove from {}.'.format(metadata.stringified_type))
        ctx.exit(code=-1)

    message_box = metadata.find_message_box(message_box_uuid)
    if message_box is None:
        click.echo('MessageBox "{}" is not registered. Do nothing.'.format(message_box_uuid))
        ctx.exit(code=-1)
    metadata.unregister_message_box(message_box)
    context_object.log_info('message box remove', uuid=message_box_uuid)
    click.echo('MessageBox "{}" is removed.'.format(message_box_uuid))
