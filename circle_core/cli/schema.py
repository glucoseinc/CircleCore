# -*- coding: utf-8 -*-
"""CLI Schema."""

# system module
from typing import TYPE_CHECKING
from uuid import UUID

# community module
import click

# project module
from .utils import output_listing_columns, output_properties
from ..models import MetaDataSession, NoResultFound, Schema, SchemaProperties

if TYPE_CHECKING:
    from typing import List, Optional, Tuple

    from click.core import Context

    from .utils import TableData, TableHeader


@click.group('schema')
def cli_schema() -> None:
    """`crcr schema`の起点."""
    pass


@cli_schema.command('list')
@click.pass_context
def schema_list(ctx: 'Context') -> None:
    """登録中のスキーマ一覧を表示する.

    Args:
        ctx: click's Context
    """
    schemas = Schema.query.all()

    if len(schemas):
        data, header = _format_for_columns(schemas)
        output_listing_columns(data, header)
    else:
        click.echo('No schemas are registered.')


def _format_for_columns(schemas: 'List[Schema]') -> 'Tuple[TableData, TableHeader]':
    """スキーマリストを表示用に加工する.

    Args:
        schemas: スキーマリスト

    Return:
        data: 加工後のスキーマリスト
        header: 見出し
    """
    header = ['UUID', 'DISPLAY_NAME', 'PROPERTIES']
    data: 'TableData' = []
    for schema in schemas:
        display_name = schema.display_name
        data.append((str(schema.uuid), display_name, schema.properties))
    return data, header


@cli_schema.command('detail')
@click.argument('schema_uuid', type=UUID)
@click.pass_context
def schema_detail(ctx: 'Context', schema_uuid: UUID) -> None:
    """スキーマの詳細を表示する.

    :param Context ctx: Context
    :param UUID schema_uuid: スキーマUUID
    """
    try:
        schema = Schema.query.filter_by(uuid=schema_uuid).one()
    except NoResultFound:
        click.echo('Schema "{}" is not registered.'.format(schema_uuid))
        ctx.exit(code=-1)

    data = [
        ('UUID', str(schema.uuid)),
        ('DISPLAY_NAME', schema.display_name),
    ]
    for i, prop in enumerate(schema.properties):
        data.append(('PROPERTIES' if i == 0 else '', '{}:{}'.format(prop.name, prop.type)))
    data.append(('MEMO', schema.memo or ''))

    boxes = schema.message_boxes
    if len(boxes):
        for i, box in enumerate(boxes):
            data.append(('Message Box' if i == 0 else '', str(box.uuid)))
        output_properties(data)
    else:
        output_properties(data)
        click.echo('No message boxes are use this schema.')


@cli_schema.command('add')
@click.option('display_name', '--name', required=True)
@click.option('memo', '--memo')
@click.argument('name_and_types', nargs=-1)
@click.pass_context
def schema_add(ctx: 'Context', display_name: str, memo: 'Optional[str]', name_and_types: 'List[str]'):
    """スキーマを登録する.

    Args:
        ctx: click's Context
        display_name: 表示名
        memo: メモ
    :param List[str] name_and_types: プロパティ
    """
    # make schema properties
    try:
        properties = SchemaProperties(name_and_types)
    except ValueError as exc:
        click.echo('Invalid properties : {}.'.format(exc))
        click.echo('Property format must be "name:type".')
        ctx.exit(code=-1)

    with MetaDataSession.begin():
        schema = Schema.create(
            display_name=display_name,
            memo=memo,
            properties=properties,
        )
        MetaDataSession.add(schema)

    click.echo('Schema "{}" is added.'.format(schema.uuid))


@cli_schema.command('remove')
@click.argument('schema_uuid', type=UUID)
@click.pass_context
def schema_remove(ctx: 'Context', schema_uuid: UUID) -> None:
    """スキーマを削除する.

    Args:
        ctx: click's Context
        schema_uuid: スキーマUUID
    """
    try:
        schema = Schema.query.filter_by(uuid=schema_uuid).one()
    except NoResultFound:
        click.echo('Schema "{}" is not registered. Do nothing.'.format(schema_uuid))
        ctx.exit(code=-1)

    with MetaDataSession.begin():
        MetaDataSession.delete(schema)

    click.echo('Schema "{}" is removed.'.format(schema_uuid))
