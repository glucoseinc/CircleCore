#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""CLI Schema."""

# community module
import click
from click.core import Context
from six import PY3

# project module
from ..models import Config, Schema
from .utils import output_listing_columns, stringify_dict


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
    config = ctx.obj['config']  # type: Config
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
    data = [[schema.uuid, schema.display_name, stringify_dict(schema.properties)]
            for schema in schemas]
    return data, header
