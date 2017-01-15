# -*- coding: utf-8 -*-

"""CLI invitation."""

# system module
import datetime
from uuid import UUID

# community module
import click
from click.core import Context
from six import PY3

# project module
from .context import ContextObject
from .utils import generate_uuid, output_listing_columns, output_properties
from ..models import Invitation

if PY3:
    from typing import List, Tuple


@click.group('invitation')
def cli_invitation():
    """`crcr invitation`の起点."""
    pass


@cli_invitation.command('list')
@click.pass_context
def invitation_list(ctx):
    """登録中のユーザ一覧を表示する.

    :param Context ctx: Context
    """
    context_object = ctx.obj  # type: ContextObject
    metadata = context_object.metadata
    invitations = metadata.invitations
    if len(invitations):
        data, header = _format_for_columns(invitations)
        output_listing_columns(data, header)
    else:
        click.echo('No invitations are registered.')


def _format_for_columns(invitations):
    """招待リストを表示用に加工する.

    :param List[invitation] invitations: スキーマリスト
    :return: data: 加工後のスキーマリスト, header: 見出し
    :rtype: Tuple[List[List[str]], List[str]]
    """
    header = ['UUID', 'MAX INVITES', 'CURRENT INVITES', 'DATE CREATED']
    data = []  # type: List[List[str]]
    for invitation in invitations:
        data.append([str(invitation.uuid), invitation.max_invites, invitation.current_invites, invitation.date_created])
    return data, header


@cli_invitation.command('detail')
@click.argument('invitation_uuid', type=UUID)
@click.pass_context
def invitation_detail(ctx, invitation_uuid):
    """招待の詳細を表示する.

    :param Context ctx: Context
    :param UUID invitation_uuid: ユーザUUID
    """
    context_object = ctx.obj  # type: ContextObject
    metadata = context_object.metadata

    invitation = metadata.find_invitation(invitation_uuid)
    if invitation is None:
        click.echo('Invitation "{}" is not registered.'.format(invitation_uuid))
        ctx.exit(code=255)

    data = [
        ('UUID', invitation.uuid),
        ('MAX INVITES', invitation.max_invites),
        ('CURRENT INVITES', invitation.current_invites),
        ('DATE CREATED', invitation.date_created.isoformat(' ') if invitation.date_created else '-----'),
    ]
    output_properties(data)


def _validate_max_invites(ctx, param, value):
    if value < 0:
        raise click.BadParameter('max_invites nees to be larger than 0')
    return value


@cli_invitation.command('add')
@click.option('max_invites', '--max', default=0, type=int, callback=_validate_max_invites)
@click.pass_context
def invitation_add(ctx, max_invites):
    """招待を登録する.

    :param Context ctx: Context
    :param int max_invites: 最大招待可能数. 0にすると無制限
    """
    context_object = ctx.obj  # type: ContextObject
    metadata = context_object.metadata

    if not metadata.writable:
        click.echo('Cannot register to {}.'.format(metadata.stringified_type))
        ctx.exit(code=-1)

    invitation = Invitation(None, max_invites, datetime.datetime.utcnow())
    metadata.register_invitation(invitation)
    context_object.log_info('Invitation add', uuid=invitation.uuid)
    click.echo('Invitation "{}" is added.'.format(invitation.uuid))


@cli_invitation.command('remove')
@click.argument('invitation_uuid', type=UUID)
@click.pass_context
def invitation_remove(ctx, invitation_uuid):
    """ユーザを削除する.

    :param Context ctx: Context
    :param UUID invitation_uuid: ユーザUUID
    """
    context_object = ctx.obj  # type: ContextObject
    metadata = context_object.metadata

    if not metadata.writable:
        click.echo('Cannot remove from {}.'.format(metadata.stringified_type))
        ctx.exit(code=-1)

    invitation = metadata.find_invitation(invitation_uuid)
    if invitation is None:
        click.echo('Invitation "{}" is not registered. Do nothing.'.format(invitation_uuid))
        ctx.exit(code=-1)
    metadata.unregister_invitation(invitation)
    context_object.log_info('invitation remove', uuid=invitation_uuid)
    click.echo('Invitation "{}" is removed.'.format(invitation_uuid))
