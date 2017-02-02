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
from .context import CLIContextObject
from .utils import output_listing_columns, output_properties
from ..models import generate_uuid, Invitation, MetaDataSession, Module, NoResultFound

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
    invitations = Invitation.query.all()
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
        data.append([str(invitation.uuid), invitation.max_invites, invitation.current_invites, invitation.created_at])
    return data, header


@cli_invitation.command('detail')
@click.argument('invitation_uuid', type=UUID)
@click.pass_context
def invitation_detail(ctx, invitation_uuid):
    """招待の詳細を表示する.

    :param Context ctx: Context
    :param UUID invitation_uuid: ユーザUUID
    """

    try:
        invitation = Invitation.query.filter_by(uuid=invitation_uuid).one()
    except NoResultFound:
        click.echo('Invitation "{}" is not registered.'.format(invitation_uuid))
        ctx.exit(code=-1)

    data = [
        ('UUID', invitation.uuid),
        ('MAX INVITES', invitation.max_invites),
        ('CURRENT INVITES', invitation.current_invites),
        ('DATE CREATED', invitation.created_at.isoformat(' ') if invitation.created_at else '-----'),
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

    with MetaDataSession.begin():
        invitation = Invitation(
            uuid=generate_uuid(model=Invitation),
            max_invites=max_invites
        )
        MetaDataSession.add(invitation)

    click.echo('Invitation "{}" is added.'.format(invitation.uuid))


@cli_invitation.command('remove')
@click.argument('invitation_uuid', type=UUID)
@click.pass_context
def invitation_remove(ctx, invitation_uuid):
    """ユーザを削除する.

    :param Context ctx: Context
    :param UUID invitation_uuid: ユーザUUID
    """
    try:
        invitation = Invitation.query.filter_by(uuid=invitation_uuid).one()
    except NoResultFound:
        click.echo('Invitation "{}" is not registered. Do nothing.'.format(invitation_uuid))
        ctx.exit(code=-1)

    with MetaDataSession.begin():
        MetaDataSession.delete(invitation)

    click.echo('Invitation "{}" is removed.'.format(invitation_uuid))
