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
from .utils import output_listing_columns, output_properties, validate_stringified_uuid_list
from ..models import MetaDataSession, NoResultFound, ReplicationLink

if PY3:
    from typing import List, Optional, Tuple


@click.group('replication_link')
def cli_replication_link():
    """`crcr replication_link`の起点."""
    pass


@cli_replication_link.command('list')
@click.pass_context
def list_replication_link(ctx):
    """登録中の共有リンク一覧を表示する.

    :param Context ctx: Context
    """
    replication_links = ReplicationLink.query.all()
    if len(replication_links):
        data, header = _format_for_columns(replication_links)
        output_listing_columns(data, header)
    else:
        click.echo('No reolication links are registered.')


def _format_for_columns(replication_links):
    """共有リンクを表示用に加工する.

    :param List[Module] replication_links: モジュールリスト
    :return: data: 加工後のリスト, header: 見出し
    :rtype: Tuple[List[List[str]], List[str]]
    """
    header = ['UUID', 'DISPLAY_NAME', 'TARGET_CORES']
    data = []  # type: List[List[str]]
    for replication_link in replication_links:
        data.append([
            str(replication_link.uuid),
            replication_link.display_name,
            ','.join(str(x) for x in replication_link.target_cores),
        ])
    return data, header


@cli_replication_link.command('detail')
@click.argument('link_uuid', type=UUID)
@click.pass_context
def show_replication_link_detail(ctx, link_uuid):
    """共有リンクの詳細を表示する.

    :param Context ctx: Context
    :param UUID link_uuid: 共有リンクUUID
    """
    replication_link = ReplicationLink.query.get(link_uuid)
    if not replication_link:
        click.echo('Replication Link "{}" is not registered.'.format(link_uuid))
        ctx.exit(code=-1)

    data = [
        ('UUID', str(replication_link.uuid)),
        ('DISPLAY_NAME', replication_link.display_name),
        ('LINK', replication_link.link),
        ('MEMO', replication_link.memo or ''),
    ]

    output_properties(data)

    click.echo('\n- TARGET CORES: -----------------------')
    for slave in replication_link.slaves:
        data = [
            ('UUID', str(slave.slave_uuid)),
        ]
        output_properties(data)

    for message_box in replication_link.message_boxes:
        click.echo('\n- MESSAGE BOX: {} ----------------------'.format(message_box.uuid))
        data = [
            ('DISPLAY_NAME', message_box.display_name),
            ('SCHEMA_UUID', str(message_box.schema_uuid)),
            ('MEMO', message_box.memo or ''),
        ]
        output_properties(data)


@cli_replication_link.command('add')
@click.option('display_name', '--name', required=True)
@click.option('--memo')
@click.option('cc_uuids', '--cc', required=True, callback=validate_stringified_uuid_list)
@click.option('message_box_uuids', '--box', callback=validate_stringified_uuid_list)
@click.option('all_boxes', '--all-boxes', is_flag=True, default=False)
@click.pass_context
def add_replication_link(ctx, display_name, memo, cc_uuids, message_box_uuids, all_boxes):
    """共有リンクを登録する.

    :param Context ctx: Context
    :param str display_name: モジュール表示名
    :param Optional[str] memo: メモ
    :param list[uuid.UUID] cc_uuids: 共有対象のCircleCoreのUUID
    :param list[uuid.UUID] message_box_uuids: 共有対象のMessageBoxのID
    :param bool all_boxes: 全Boxを共有する場合はTrue
    """
    if not all_boxes and not message_box_uuids:
        raise click.BadParameter('Please specify box uuids or all flag')
    if all_boxes and message_box_uuids:
        raise click.BadParameter('Both box flag has specified')
    if all_boxes:
        message_box_uuids = ReplicationLink.ALL_MESSAGE_BOXES
    else:
        message_box_uuids = validate_stringified_uuid_list(ctx, None, message_box_uuids)

    with MetaDataSession.begin():
        replication_link = ReplicationLink.create(
            display_name=display_name,
            memo=memo,
            slaves=cc_uuids,
            message_box_uuids=message_box_uuids,
        )
        print('replication_link', replication_link)
        print(replication_link.message_boxes)
        MetaDataSession.add(replication_link)

    click.echo('Replication Link "{}" is added.'.format(replication_link.uuid))


@cli_replication_link.command('remove')
@click.argument('link_uuid', type=UUID)
@click.pass_context
def remove_replication_link(ctx, link_uuid):
    """共有リンクを削除する.

    :param Context ctx: Context
    :param UUID module_uuid: モジュールUUID
    """
    replication_link = ReplicationLink.query.get(link_uuid)
    if not replication_link:
        click.echo('Module "{}" is not registered. Do nothing.'.format(module_uuid))
        ctx.exit(code=-1)

    with MetaDataSession.begin():
        MetaDataSession.delete(replication_link)

    click.echo('Replication Link "{}" is removed.'.format(replication_link.uuid))
