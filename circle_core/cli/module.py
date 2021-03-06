# -*- coding: utf-8 -*-
"""CLI Module."""

# system module
from typing import TYPE_CHECKING
from uuid import UUID

# community module
import click

# project module
from .utils import output_listing_columns, output_properties
from ..models import MetaDataSession, Module, NoResultFound

if TYPE_CHECKING:
    from typing import List, Optional, Tuple

    from click.core import Context

    from .utils import TableData, TableHeader


@click.group('module')
def cli_module() -> None:
    """`crcr module`の起点."""
    pass


@cli_module.command('list')
@click.pass_context
def module_list(ctx: 'Context'):
    """登録中のモジュール一覧を表示する.

    :param Context ctx: Context
    """
    modules = Module.query.all()
    if len(modules):
        data, header = _format_for_columns(modules)
        output_listing_columns(data, header)
    else:
        click.echo('No modules are registered.')


def _format_for_columns(modules: 'List[Module]') -> 'Tuple[TableData, TableHeader]':
    """モジュールリストを表示用に加工する.

    Args:
        modules: モジュールリスト
    Return:
        data: 加工後のモジュールリスト, header: 見出し
    """
    header = ['UUID', 'DISPLAY_NAME', 'TAGS', 'ATTRIBUTES']
    data: 'TableData' = []
    for module in modules:
        display_name = module.display_name
        data.append((
            str(module.uuid),
            display_name,
            ','.join(module.tags),
            module.attributes,
        ))
    return data, header


@cli_module.command('detail')
@click.argument('module_uuid', type=UUID)
@click.pass_context
def module_detail(ctx: 'Context', module_uuid: UUID) -> None:
    """モジュールの詳細を表示する.

    :param Context ctx: Context
    :param UUID module_uuid: モジュールUUID
    """
    try:
        module = Module.query.filter_by(uuid=module_uuid).one()  # type: Module
    except NoResultFound:
        click.echo('Module "{}" is not registered.'.format(module_uuid))
        ctx.exit(code=-1)

    data = [
        ('UUID', str(module.uuid)),
        ('DISPLAY_NAME', module.display_name),
    ]

    for i, tag in enumerate(module.tags):
        data.append(('TAG' if i == 0 else '', tag))

    for i, attribute in enumerate(module.attributes):
        data.append(('ATTRIBUTE' if i == 0 else '', attribute))

    data.append(('MEMO', module.memo or ''))

    output_properties(data)

    for message_box in module.message_boxes:
        click.echo('\n- MESSAGE BOX: {} ----------------------'.format(message_box.uuid))
        data = [
            ('DISPLAY_NAME', message_box.display_name),
            ('SCHEMA_UUID', str(message_box.schema_uuid)),
            ('MEMO', message_box.memo or ''),
        ]
        output_properties(data)


@cli_module.command('add')
@click.option('display_name', '--name', required=True)
@click.option('attributes', '--attribute')
@click.option('tags', '--tag')
@click.option('--memo')
@click.pass_context
def module_add(
    ctx: 'Context', display_name: str, attributes: 'Optional[str]', tags: 'Optional[str]', memo: 'Optional[str]'
):
    """モジュールを登録する.

    :param Context ctx: Context
    :param str display_name: モジュール表示名
    :param Optional[str] attributes: 属性
    :param Optional[str] tags: タグ
    :param Optional[str] memo: メモ
    """

    with MetaDataSession.begin():
        module = Module.create(
            display_name=display_name,
            attributes=attributes,
            tags=tags,
            memo=memo,
        )
        MetaDataSession.add(module)

    click.echo('Module "{}" is added.'.format(module.uuid))


@cli_module.command('remove')
@click.argument('module_uuid', type=UUID)
@click.pass_context
def module_remove(ctx: 'Context', module_uuid):
    """モジュールを削除する.

    :param Context ctx: Context
    :param UUID module_uuid: モジュールUUID
    """
    try:
        module = Module.query.filter_by(uuid=module_uuid).one()
    except NoResultFound:
        click.echo('Module "{}" is not registered. Do nothing.'.format(module_uuid))
        ctx.exit(code=-1)

    with MetaDataSession.begin():
        MetaDataSession.delete(module)

    click.echo('Module "{}" is removed.'.format(module_uuid))
