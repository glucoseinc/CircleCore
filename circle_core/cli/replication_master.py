# -*- coding: utf-8 -*-
"""CLI Module."""

# system module
from uuid import UUID

# community module
import click
from click.core import Context
from six import PY3

# project module
from .context import CLIContextObject
from .utils import output_listing_columns, output_properties
from ..models import generate_uuid, MetaDataSession, NoResultFound, ReplicationMaster

if PY3:
    from typing import List, Optional, Tuple


@click.group('replication_master')
def cli_replication_master():
    """`crcr master`の起点."""
    pass


@cli_replication_master.command('list')
@click.pass_context
def list_replication_masters(ctx):
    """登録中のモジュール一覧を表示する.

    :param Context ctx: Context
    """
    objects = ReplicationMaster.query.all()
    if len(objects):
        data, header = _format_for_columns(objects)
        output_listing_columns(data, header)
    else:
        click.echo('No replication masters are registered.')


def _format_for_columns(objects):
    """モジュールリストを表示用に加工する.

    :param List[Module] modules: モジュールリスト
    :return: data: 加工後のモジュールリスト, header: 見出し
    :rtype: Tuple[List[List[str]], List[str]]
    """
    header = ['ENDPOINT']
    data = []  # type: List[List[str]]
    for obj in objects:
        data.append([
            obj.endpoint_url,
        ])
    return data, header


@cli_replication_master.command('add')
@click.option('endpoint', '--endpoint', required=True)
@click.pass_context
def add_replication_master(ctx, endpoint):
    """共有マスターを登録する.

    :param Context ctx: Context
    :param str endpoint: モジュール表示名
    """

    # TODO: check endpoint is valid url
    with MetaDataSession.begin():
        obj = ReplicationMaster(endpoint_url=endpoint)
        MetaDataSession.add(obj)

    click.echo('Replication Master "{}" is added.'.format(obj.endpoint_url))
