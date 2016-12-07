# -*- coding: utf-8 -*-

"""CLI User."""

# system module
from uuid import UUID

# community module
import click
from click.core import Context
from six import PY3

# project module
from .context import ContextObject
from .utils import generate_uuid, output_listing_columns, output_properties
from ..models import User
from ..models.user import encrypt_password

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
    context_object = ctx.obj  # type: ContextObject
    metadata = context_object.metadata
    users = metadata.users
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
    header = ['UUID', 'EMAIL', 'PERMISSIONS']
    data = []  # type: List[List[str]]
    for user in users:
        data.append([str(user.uuid), user.mail_address, user.stringified_permissions])
    return data, header


@cli_user.command('detail')
@click.argument('user_uuid', type=UUID)
@click.pass_context
def user_detail(ctx, user_uuid):
    """ユーザの詳細を表示する.

    :param Context ctx: Context
    :param UUID user_uuid: ユーザUUID
    """
    context_object = ctx.obj  # type: ContextObject
    metadata = context_object.metadata

    user = metadata.find_user(user_uuid)
    if user is None:
        click.echo('User "{}" is not registered.'.format(user_uuid))
        ctx.exit(code=-1)

    data = [
        ('UUID', str(user.uuid)),
        ('EMAIL', user.mail_address),
    ]
    for i, permission in enumerate(user.permissions):
        data.append(('PERMISSIONS' if i == 0 else '', permission))

    output_properties(data)


@cli_user.command('add')
@click.option('mail_address', '--email', required=True)
@click.option('--password', required=True)
@click.option('admin_flag', '--admin', is_flag=True, default=False)
@click.pass_context
def user_add(ctx, mail_address, password, admin_flag):
    """ユーザを登録する.

    :param Context ctx: Context
    :param str mail_address: メールアドレス
    :param str password: パスワード
    :param bool admin_flag: ユーザ管理権限
    """
    context_object = ctx.obj  # type: ContextObject
    metadata = context_object.metadata

    if not metadata.writable:
        click.echo('Cannot register to {}.'.format(metadata.stringified_type))
        ctx.exit(code=-1)

    user_uuid = generate_uuid(existing=[user.uuid for user in metadata.users])

    permissions = []
    if admin_flag:
        permissions.append('admin')

    encrypted_password = encrypt_password(password, user_uuid.hex)
    user = User(user_uuid, mail_address, encrypted_password, ','.join(permissions))

    metadata.register_user(user)
    context_object.log_info('user add', uuid=user.uuid)
    click.echo('User "{}" is added.'.format(user.uuid))


@cli_user.command('remove')
@click.argument('user_uuid', type=UUID)
@click.pass_context
def user_remove(ctx, user_uuid):
    """ユーザを削除する.

    :param Context ctx: Context
    :param UUID user_uuid: ユーザUUID
    """
    context_object = ctx.obj  # type: ContextObject
    metadata = context_object.metadata

    if not metadata.writable:
        click.echo('Cannot remove from {}.'.format(metadata.stringified_type))
        ctx.exit(code=-1)

    user = metadata.find_user(user_uuid)
    if user is None:
        click.echo('User "{}" is not registered. Do nothing.'.format(user_uuid))
        ctx.exit(code=-1)
    metadata.unregister_user(user)
    context_object.log_info('user remove', uuid=user_uuid)
    click.echo('User "{}" is removed.'.format(user_uuid))
