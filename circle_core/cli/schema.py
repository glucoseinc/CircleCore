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
from .utils import output_listing_columns, output_properties
from ..models import Schema
from ..models.config import ConfigRedis

if PY3:
    from typing import List, Optional, Tuple


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
    data = []  # type: List[List[str]]
    for schema in schemas:
        display_name = schema.display_name if schema.display_name is not None else ''
        data.append([schema.uuid, display_name, schema.stringified_properties])
    return data, header


@cli_schema.command('detail')
@click.argument('schema_uuid')
@click.pass_context
def schema_detail(ctx, schema_uuid):
    """スキーマの詳細を表示する.

    :param Context ctx: Context
    :param str schema_uuid: スキーマUUID
    """
    context_object = ctx.obj  # type: ContextObject
    config = context_object.config

    schema = config.matched_schema(schema_uuid)
    if schema is None:
        click.echo('Schema "{}" is not registered.'.format(schema_uuid))
        ctx.exit(code=-1)

    data = [
        ('UUID', schema.uuid),
        ('DISPLAY_NAME', schema.display_name),
    ]
    for i, prop in enumerate(schema.properties):
        data.append(('PROPERTIES' if i == 0 else '', '{}:{}'.format(prop.name, prop.type)))

    devices = [device for device in config.devices if device.schema_uuid == schema_uuid]
    if len(devices):
        for i, device in enumerate(devices):
            data.append(('Devices' if i == 0 else '', device.display_name))
        output_properties(data)
    else:
        output_properties(data)
        click.echo('No devices are use this schema.')


@cli_schema.command('add')
@click.option('display_name', '--name')
@click.argument('name_and_types', nargs=-1)
@click.pass_context
def schema_add(ctx, display_name, name_and_types):
    """スキーマを登録する.

    :param Context ctx: Context
    :param Optional[str] display_name: 表示名
    :param List[str] name_and_types: プロパティ
    """
    context_object = ctx.obj  # type: ContextObject
    config = context_object.config

    if not isinstance(config, (ConfigRedis,)):
        click.echo('Cannot register to {}.'.format(config.stringified_type))
        ctx.exit(code=-1)

    schema_uuid = str(uuid4())
    # TODO: 重複チェックする

    properties = {}
    for i, name_and_type in enumerate(name_and_types, start=1):
        splitted = name_and_type.split(':')
        if len(splitted) != 2:
            click.echo('Argument is invalid : {}.'.format(name_and_type))
            click.echo('Argument format must be "name:type"')
            ctx.exit(code=-1)
        _name, _type = splitted[0], splitted[1]
        properties['key{}'.format(i)] = _name
        properties['type{}'.format(i)] = _type
    schema = Schema(schema_uuid, display_name, **properties)

    if isinstance(config, ConfigRedis):
        redis_client = config.redis_client
        if redis_client is None:
            click.echo('Cannot connect to Redis server.')
            ctx.exit(code=-1)

        schema.register_to_redis(redis_client)
        click.echo('Schema "{}" is added.'.format(schema.uuid))


@cli_schema.command('remove')
@click.argument('schema_uuid')
@click.pass_context
def schema_remove(ctx, schema_uuid):
    """スキーマを削除する.

    :param Context ctx: Context
    :param str schema_uuid: スキーマUUID
    """
    context_object = ctx.obj  # type: ContextObject
    config = context_object.config

    if not isinstance(config, (ConfigRedis,)):
        click.echo('Cannot remove from {}.'.format(config.stringified_type))
        ctx.exit(code=-1)

    if isinstance(config, ConfigRedis):
        redis_client = config.redis_client
        schema = config.matched_schema(schema_uuid)
        if schema is None:
            click.echo('Schema "{}" is not registered. Do nothing.'.format(schema_uuid))
            ctx.exit(code=-1)
        schema.unregister_from_redis(redis_client)
        click.echo('Schema "{}" is removed.'.format(schema_uuid))
