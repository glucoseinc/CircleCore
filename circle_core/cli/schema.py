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
    data = [[schema.uuid, schema.display_name, schema.stringified_properties]
            for schema in schemas]
    return data, header


@cli_schema.command('detail')
@click.argument('schema_uuid')
@click.pass_context
def schema_detail(ctx, schema_uuid):
    """スキーマの詳細を表示する.

    :param Context ctx: Context
    :param str schema_uuid: スキーマUUID
    """
    # TODO: 表示の整形を関数化
    context_object = ctx.obj  # type: ContextObject
    config = context_object.config

    schema = _get_matching_schema(config.schemas, schema_uuid)
    if schema is None:
        click.echo('Schema "{}" is not registered.'.format(schema_uuid))
        ctx.exit(code=-1)
    click.echo('UUID         : {}'.format(schema.uuid))
    click.echo('DISPLAY_NAME : {}'.format(schema.display_name))
    for i, prop in enumerate(schema.properties):
        click.echo('{}   : {}:{}'.format('PROPERTIES' if i == 0 else ' ' * len('PROPERTIES'), prop.name, prop.type))

    devices = [device for device in config.devices if device.schema_uuid == schema_uuid]
    if len(devices):
        click.echo('Devices which use this schema : {}'.format(', '.join([device.display_name for device in devices])))
    else:
        click.echo('No devices are use this schema.')


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
        click.echo('Cannot register to {}.'.format(config.stringified_type))
        ctx.exit(code=-1)

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
            click.echo('Cannot connect to Redis server.')
            ctx.exit(code=-1)

        # 登録されていない最小の数を取得する
        registered_nums = [_schema.db_id for _schema in config.schemas]
        for num in range(1, len(registered_nums) + 2):
            if num not in registered_nums:
                break
        schema.db_id = num
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

    if config.type not in (ConfigType.redis,):
        click.echo('Cannot remove from {}.'.format(config.stringified_type))
        ctx.exit(code=-1)

    if config.type == ConfigType.redis:
        redis_client = config.redis_client
        schema = _get_matching_schema(config.schemas, schema_uuid)
        if schema is None:
            click.echo('Schema "{}" is not registered. Do nothing.'.format(schema_uuid))
            ctx.exit(code=-1)
        schema.unregister_from_redis(redis_client)
        click.echo('Schema "{}" is removed.'.format(schema_uuid))


def _get_matching_schema(schemas, schema_uuid):
    """スキーマ一覧からUUIDがマッチするスキーマを取得する.
    :param List[Schema] schemas: 検索対象のスキーマ一覧
    :param str schema_uuid: 取得するスキーマのUUID
    :return: マッチしたスキーマ
    :rtype: Optional[Schema]
    """
    schemas = [schema for schema in schemas if schema.uuid == schema_uuid]
    return schemas[0] if len(schemas) != 0 else None
