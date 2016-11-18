#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""CLI Schema."""

# system module
from uuid import uuid4

# community module
import click
from click.core import Context
from six import PY3

# project module
from .context import ContextObject
from .utils import output_listing_columns
from ..models import Schema
from ..models.config import ConfigType

if PY3:
    from typing import List, Tuple


@click.group('schema')
@click.pass_context
def cli_schema(ctx):
    """`crcr schema`の起点.

    :param Context ctx: Context
    """
    pass


@cli_schema.command('list')
@click.pass_context
def schema_list(ctx):
    """登録中のスキーマ一覧を表示する.

    :param Context ctx: Context
    """
    context_object = ctx.obj  # type: ContextObject
    config = context_object.config
    schemas = config.schemas
    if len(schemas):
        data, header = _format_for_columns(schemas)
        output_listing_columns(data, header)
    else:
        click.echo('No schemas are registered.')


def _format_for_columns(schemas):
    """スキーマリストを表示用に加工する.

    :param List[Schema] schemas: スキーマリスト
    :return: data: 加工後のスキーマリスト, header: 見出し
    :rtype: Tuple[List[List[str]], List[str]]
    """
    header = ['UUID', 'DISPLAY_NAME', 'PROPERTIES']
    data = [[schema.uuid, schema.display_name, schema.stringified_properties]
            for schema in schemas]
    return data, header


@cli_schema.command('add')
@click.argument('display_name')
@click.argument('name_and_types', nargs=-1)
@click.pass_context
def schema_add(ctx, display_name, name_and_types):
    """スキーマを登録する.

    :param Context ctx: Context
    :param str display_name: 表示名
    :param List[str] name_and_types: プロパティ
    """
    context_object = ctx.obj  # type: ContextObject
    config = context_object.config

    if config.type not in (ConfigType.redis,):
        click.echo('{} には登録できません.'.format(config._type))
        ctx.exit()

    schema_uuid = str(uuid4())
    # TODO: 重複チェックする

    properties = {}
    for i, name_and_type in enumerate(name_and_types, start=1):
        _name, _type = name_and_type.split(':')
        properties['key{}'.format(i)] = _name
        properties['type{}'.format(i)] = _type
    schema = Schema(schema_uuid, display_name, **properties)

    if config.type == ConfigType.redis:
        redis_client = config.redis_client
        if redis_client is None:
            click.echo('Redisサーバに接続できません.')
            ctx.exit()
        schema.register_to_redis(redis_client)
        click.echo('Added.')
