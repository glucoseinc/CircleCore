#!/usr/bin/env python
# -*- coding: utf-8 -*-

# community module
import click
from six import PY3

# project module
from ..models import Config, Schema  # noqa
from .utils import output_listing_columns, stringify_dict


if PY3:
    from typing import List, Tuple  # noqa


@click.group('schema')
@click.pass_context
def cli_schema(ctx):
    # type: (Any) -> None
    pass


@cli_schema.command('list')
@click.pass_context
def schema_list(ctx):
    # type: (Any) -> None
    config = ctx.obj['config']  # type: Config
    schemas = config.schemas
    if len(schemas):
        data, header = _format_for_columns(schemas)
        output_listing_columns(data, header)
    else:
        click.echo('No schemas are registered.')


def _format_for_columns(schemas):
    # type: (List[Schema]) -> Tuple[List[List[str]], List[str]]
    header = ['UUID', 'DISPLAY_NAME', 'PROPERTIES']
    data = [[schema.uuid, schema.display_name, stringify_dict(schema.properties)]
            for schema in schemas]
    return data, header
