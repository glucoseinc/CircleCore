# -*- coding: utf-8 -*-
"""CLI Module."""

# system module
from typing import TYPE_CHECKING

# community module
import click
from click.core import Context

# project module
from .utils import output_listing_columns
from ..models import MetaDataSession, ReplicationMaster

if TYPE_CHECKING:
    from typing import List, Tuple

    from .utils import TableData, TableHeader


@click.group('replication_master')
def cli_replication_master() -> None:
    """`crcr master`の起点."""
    pass


@cli_replication_master.command('list')
@click.pass_context
def list_replication_masters(ctx: 'Context') -> None:
    """登録中のモジュール一覧を表示する.

    Args:
        ctx: Context
    """
    objects = ReplicationMaster.query.all()
    if len(objects):
        data, header = _format_for_columns(objects)
        output_listing_columns(data, header)
    else:
        click.echo('No replication masters are registered.')


def _format_for_columns(objects: 'List[ReplicationMaster]') -> 'Tuple[TableData, TableHeader]':
    """ReplicationMasterリストを表示用に加工する.

    Args:
        objects: ReplicationMaster list

    Return:
        data: 加工後のモジュールリスト, header: 見出し
    """
    header = ['ENDPOINT']
    data: 'TableData' = []
    for obj in objects:
        data.append((obj.endpoint_url,))
    return data, header


@cli_replication_master.command('add')
@click.option('endpoint', '--endpoint', required=True)
@click.pass_context
def add_replication_master(ctx: 'Context', endpoint: str) -> None:
    """共有マスターを登録する.

    :param Context ctx: Context
    :param str endpoint: モジュール表示名
    """

    # TODO: check endpoint is valid url
    with MetaDataSession.begin():
        obj = ReplicationMaster(endpoint_url=endpoint)
        MetaDataSession.add(obj)

    click.echo('Replication Master "{}" is added.'.format(obj.endpoint_url))
