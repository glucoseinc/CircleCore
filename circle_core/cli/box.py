# -*- coding: utf-8 -*-
"""CLI Box."""

# system module
from typing import TYPE_CHECKING
from uuid import UUID

# community module
import click

# project module
from .utils import output_listing_columns, output_properties
from ..models import MessageBox, MetaDataSession, Module, NoResultFound, Schema, generate_uuid

if TYPE_CHECKING:
    from typing import List, Tuple

    from click.core import Context

    from .utils import TableData, TableHeader


@click.group('box')
def cli_box() -> None:
    """`crcr box`の起点."""
    pass


@cli_box.command('list')
@click.pass_context
def box_list(ctx: 'Context') -> None:
    """登録中のメッセージボックス一覧を表示する.

    :param Context ctx: Context
    """
    message_boxes = MessageBox.query.all()
    if len(message_boxes):
        data, header = _format_for_columns(message_boxes)
        output_listing_columns(data, header)
    else:
        click.echo('No message boxes are registered.')


def _format_for_columns(message_boxes: 'List[MessageBox]') -> 'Tuple[TableData, TableHeader]':
    """メッセージボックスリストを表示用に加工する.

    Args:
        message_boxes: メッセージボックスリスト
    Return:
        data: 加工後のメッセージボックスリスト, header: 見出し
    """
    header = ['UUID', 'DISPLAY_NAME']
    data: 'TableData' = []
    for message_box in message_boxes:
        display_name = message_box.display_name
        data.append((
            str(message_box.uuid),
            display_name,
        ))
    return data, header


@cli_box.command('detail')
@click.argument('message_box_uuid', type=UUID)
@click.pass_context
def box_detail(ctx: 'Context', message_box_uuid):
    """モジュールの詳細を表示する.

    :param Context ctx: Context
    :param UUID message_box_uuid: モジュールUUID
    """
    try:
        message_box = MessageBox.query.filter_by(uuid=message_box_uuid).one()
    except NoResultFound:
        click.echo('MessageBox "{}" is not registered.'.format(message_box_uuid))
        ctx.exit(code=-1)

    data = [
        ('UUID', str(message_box.uuid)),
        ('DISPLAY_NAME', message_box.display_name),
        ('SCHEMA_UUID', str(message_box.schema_uuid)),
        ('MODULE_UUID', str(message_box.module_uuid)),
        ('MEMO', message_box.memo or ''),
    ]

    output_properties(data)


@cli_box.command('add')
@click.option('display_name', '--name', required=True)
@click.option('schema_uuid', '--schema', type=UUID, required=True)
@click.option('module_uuid', '--module', type=UUID, required=True)
@click.option('--memo')
@click.pass_context
def box_add(ctx: 'Context', display_name, schema_uuid, module_uuid, memo):
    """メッセージボックスを登録する.

    :param Context ctx: Context
    :param str display_name: モジュール表示名
    :param UUID schema_uuid: スキーマUUID
    :param UUID module_uuid: スキーマUUID
    :param str memo: メモ
    """

    try:
        Schema.query.filter_by(uuid=schema_uuid).one()
    except NoResultFound:
        click.echo('Schema "{}" is not exist. Do nothing.'.format(schema_uuid))
        ctx.exit(code=-1)

    try:
        Module.query.filter_by(uuid=module_uuid).one()
    except NoResultFound:
        click.echo('Module "{}" is not exist. Do nothing.'.format(module_uuid))
        ctx.exit(code=-1)

    with MetaDataSession.begin():
        message_box = MessageBox(
            uuid=generate_uuid(model=MessageBox),
            display_name=display_name,
            schema_uuid=schema_uuid,
            module_uuid=module_uuid,
            memo=memo
        )
        MetaDataSession.add(message_box)

    click.echo('MessageBox "{}" is added.'.format(message_box.uuid))


@cli_box.command('remove')
@click.argument('message_box_uuid', type=UUID)
@click.pass_context
def box_remove(ctx: 'Context', message_box_uuid):
    """モジュールを削除する.

    :param Context ctx: Context
    :param UUID message_box_uuid: モジュールUUID
    """
    try:
        message_box = MessageBox.query.filter_by(uuid=message_box_uuid).one()
    except NoResultFound:
        click.echo('MessageBox "{}" is not registered. Do nothing.'.format(message_box_uuid))
        ctx.exit(code=-1)

    with MetaDataSession.begin():
        MetaDataSession.delete(message_box)

    click.echo('MessageBox "{}" is removed.'.format(message_box_uuid))
