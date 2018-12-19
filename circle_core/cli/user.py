# -*- coding: utf-8 -*-
"""CLI User."""

# system module
from typing import TYPE_CHECKING
from uuid import UUID

# community module
import click

# project module
from .utils import output_listing_columns, output_properties
from ..models import MetaDataSession, NoResultFound, User, generate_uuid

if TYPE_CHECKING:
    from typing import List, Tuple

    from click.core import Context

    from .utils import TableData, TableHeader


@click.group('user')
def cli_user():
    """`crcr user`の起点."""
    pass


@cli_user.command('list')
@click.pass_context
def user_list(ctx: 'Context'):
    """登録中のユーザ一覧を表示する.

    :param Context ctx: Context
    """
    users = User.query.all()

    if len(users):
        data, header = _format_for_columns(users)
        output_listing_columns(data, header)
    else:
        click.echo('No users are registered.')


def _format_for_columns(users: 'List[User]') -> 'Tuple[TableData, TableHeader]':
    """ユーザリストを表示用に加工する.

    Args:
        users: スキーマリスト
    Return:
        data: 加工後のスキーマリスト, header: 見出し
    """
    header = ['UUID', 'ACCOUNT', 'PERMISSIONS']
    data: 'TableData' = []
    for user in users:
        data.append((str(user.uuid), user.account, ','.join(user.permissions)))
    return data, header


@cli_user.command('detail')
@click.argument('user_uuid', type=UUID)
@click.pass_context
def user_detail(ctx: 'Context', user_uuid):
    """ユーザの詳細を表示する.

    :param Context ctx: Context
    :param UUID user_uuid: ユーザUUID
    """
    try:
        user = User.query.filter_by(uuid=user_uuid).one()
    except NoResultFound:
        click.echo('User "{}" is not registered.'.format(user_uuid))
        ctx.exit(code=-1)

    data = [
        ('UUID', str(user.uuid)),
        ('ACCOUNT', user.account),
        ('WORK', user.work),
        ('MAIL ADDRESS', user.mail_address),
        ('TELEPHONE', user.telephone),
    ]
    for i, permission in enumerate(user.permissions):
        data.append(('PERMISSIONS' if i == 0 else '', permission))

    output_properties(data)


@cli_user.command('add')
@click.option('account', '--account', required=True)
@click.option('password', '--password', required=True, prompt=True, hide_input=True, confirmation_prompt=True)
@click.option('work', '--work', default='')
@click.option('mail_address', '--email', default='')
@click.option('telephone', '--telephone', default='')
@click.option('admin_flag', '--admin', is_flag=True, default=False)
@click.pass_context
def user_add(ctx: 'Context', account, password, work, mail_address, telephone, admin_flag):
    """ユーザを登録する.

    :param Context ctx: Context
    :param str mail_address: メールアドレス
    :param str password: パスワード
    :param bool admin_flag: ユーザ管理権限
    """
    permissions = []
    if admin_flag:
        permissions.append('admin')

    with MetaDataSession.begin():
        user = User(
            uuid=generate_uuid(model=User),
            account=account,
            password=password,
            work=work,
            mail_address=mail_address,
            telephone=telephone,
        )
        user.permissions = permissions
        MetaDataSession.add(user)

    click.echo('User "{}" is added.'.format(user.uuid))


@cli_user.command('remove')
@click.argument('user_uuid', type=UUID)
@click.pass_context
def user_remove(ctx: 'Context', user_uuid):
    """ユーザを削除する.

    :param Context ctx: Context
    :param UUID user_uuid: ユーザUUID
    """
    try:
        user = User.query.filter_by(uuid=user_uuid).one()
    except NoResultFound:
        click.echo('User "{}" is not registered. Do nothing.'.format(user_uuid))
        ctx.exit(code=-1)

    with MetaDataSession.begin():
        MetaDataSession.delete(user)

    click.echo('User "{}" is removed.'.format(user_uuid))


@cli_user.command('change_password')
@click.option('new_password', '--new-password', prompt=True, hide_input=True, confirmation_prompt=True)
@click.argument('user_uuid', type=UUID)
@click.pass_context
def user_change_password(ctx: 'Context', user_uuid, new_password):
    """ユーザのパスワードを変更する

    :param Context ctx: Context
    :param UUID user_uuid: ユーザUUID
    :param str new_password: 新しいパスワード
    """
    try:
        user = User.query.filter_by(uuid=user_uuid).one()
    except NoResultFound:
        click.echo('User "{}" is not registered. Do nothing.'.format(user_uuid))
        ctx.exit(code=-1)

    with MetaDataSession.begin():
        user.set_password(new_password)
        MetaDataSession.add(user)

    click.echo('User "{}"\'s password is changed.'.format(user_uuid))
