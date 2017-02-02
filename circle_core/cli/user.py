# -*- coding: utf-8 -*-

"""CLI User."""

# system module
from uuid import UUID

# community module
import click
from click.core import Context
from six import PY3

# project module
from .context import CLIContextObject
from .utils import output_listing_columns, output_properties
from ..models import generate_uuid, MetaDataSession, NoResultFound, User

if PY3:
    from typing import List, Tuple


@click.group('user')
def cli_user():
    """`crcr user`の起点."""
    pass


@cli_user.command('list')
@click.pass_context
def user_list(ctx):
    """登録中のユーザ一覧を表示する.

    :param Context ctx: Context
    """
    users = User.query.all()

    if len(users):
        data, header = _format_for_columns(users)
        output_listing_columns(data, header)
    else:
        click.echo('No users are registered.')


def _format_for_columns(users):
    """ユーザリストを表示用に加工する.

    :param List[User] users: スキーマリスト
    :return: data: 加工後のスキーマリスト, header: 見出し
    :rtype: Tuple[List[List[str]], List[str]]
    """
    header = ['UUID', 'ACCOUNT', 'PERMISSIONS']
    data = []  # type: List[List[str]]
    for user in users:
        data.append([str(user.uuid), user.account, ','.join(user.permissions)])
    return data, header


@cli_user.command('detail')
@click.argument('user_uuid', type=UUID)
@click.pass_context
def user_detail(ctx, user_uuid):
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
def user_add(ctx, account, password, work, mail_address, telephone, admin_flag):
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
def user_remove(ctx, user_uuid):
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
