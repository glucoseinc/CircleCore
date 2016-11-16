#!/usr/bin/env python
# -*- coding: utf-8 -*-

# system module
from unicodedata import east_asian_width

# community module
import click
from six import PY2

# project module
from ..models import Config, Device  # noqa


if PY2:
    from itertools import izip_longest as zip_longest
else:
    from itertools import zip_longest
    from typing import List, Tuple  # noqa


@click.group('device')
@click.pass_context
def cli_device(ctx):
    # type: (Any) -> None
    pass


@cli_device.command('list')
@click.pass_context
def device_list(ctx):
    # type: (Any) -> None
    config = ctx.obj['config']  # type: Config
    devices = config.devices
    if len(devices):
        data, header = format_for_columns(devices)
        output_listing_columns(data, header)
    else:
        click.echo('No devices are registered.')


def format_for_columns(devices):
    # type: (List[Device]) -> Tuple[List[List[str]], List[str]]
    header = ['SCHEMA', 'DISPLAY_NAME', 'PROPERTIES']

    data = []

    for device in devices:
        row = [device.schema_uuid, device.display_name]
        properties = []
        for k, v in device.properties.items():
            properties.append('{}:{}'.format(k, v))
        row.append(', '.join(properties))
        data.append(row)

    return data, header


def output_listing_columns(data, header):
    # type: (List[List[str]], List[str]) -> None
    if len(data) > 0:
        data.insert(0, header)

    row_strings, sizes = create_row_strings(data)

    # Create and add a separator.
    if len(data) > 0:
        separator = ' '.join(['-' * size for size in sizes])
        row_strings.insert(1, separator)

    # Display rows.
    for row_string in row_strings:
        click.echo(row_string)


def create_row_strings(rows):
    # type: (List[List[str]]) -> Tuple[List[str], List[int]]
    def _len(string):
        # type: (str) -> int
        if PY2:
            string = string.decode('utf-8')
        return sum([1 if 'NaH'.count(east_asian_width(char)) > 0 else 2
                    for char in string])

    def _ljust(size, string):
        # type: (int, str) -> str
        return string + ' ' * (size - _len(string))

    assert len(rows) > 0

    # Calculate columns size.
    sizes = [0] * max(len(x) for x in rows)
    for row in rows:
        sizes = [max(size, _len(string)) for size, string in zip_longest(sizes, row)]

    # Create row strings.
    row_strings = []
    for row in rows:
        row_string = ' '.join([_ljust(size, string) if string is not None else ''
                               for size, string in zip_longest(sizes, row)])
        row_strings.append(row_string)

    return row_strings, sizes
