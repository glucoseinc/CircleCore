# -*- coding: utf-8 -*-

"""CLI Main."""

# system module
from __future__ import absolute_import, print_function

from itertools import groupby
import logging
import os
import re
import sys

# community module
import click
from click.core import Context

# project module
# from circle_core import server
from circle_core.core import CircleCore
from .context import CLIContextObject
from ..database import Database


logger = logging.getLogger(__name__)


@click.group()
@click.option('config_file_path', '--config', '-c', type=click.Path())
@click.option('--debug', is_flag=True)
@click.pass_context
def cli_main(ctx, config_file_path, debug):
    """`crcr`の起点.

    :param Context ctx: Context
    :param str config_file_path: iniファイルのpath
    """
    # initialize console logging
    _init_logging(debug)

    if config_file_path:
        core = CircleCore.load_from_config_file(config_file_path, debug)
    else:
        core = CircleCore.load_from_default_config_file(debug)

    ctx.obj = CLIContextObject(core)


def _init_logging(debug=False):
    if sys.stderr.isatty():
        # if we are attached to tty, use colorful.
        fh = logging.StreamHandler(sys.stderr)
        try:
            from ..logger import NiceColoredFormatter
            # 色指示子で9charsとる
            fh.setFormatter(NiceColoredFormatter(
                '%(nice_levelname)-14s %(nice_name)-33s: %(message)s',
            ))
        except ImportError:
            fh.setFormatter(logging.Formatter(
                '%(levelname)-5s %(name)-24s: %(message)s',
            ))

        root_logger = logging.getLogger()
        root_logger.addHandler(fh)
        root_logger.setLevel(logging.DEBUG if debug else logging.INFO)


@cli_main.command('env')
@click.pass_context
def cli_main_env(ctx):
    """CircleCoreの環境を表示する.

    :param Context ctx: Context
    """
    core = ctx.obj.core

    click.echo(
        'Circle Core: {display_name}({uuid})'.format(
            display_name=core.my_cc_info.display_name,
            uuid=core.my_cc_info.uuid))
    click.echo('Metadata File path: {}'.format(core.metadata_file_path))
    click.echo('Log File path: {}'.format(core.log_file_path))


def validate_replication_master_addr(ctx, param, values):
    for addr in values:
        if re.search(r'^[0-9A-Fa-f-]+@.+\:\d+$', addr) is None:
            raise click.BadParameter('You must specify --replicate like module_uuid@hostname:port')

    return values


@cli_main.command('run')
@click.pass_context
def cli_main_run(ctx):
    """CircleCoreの起動."""
    # ctx.obj.ipc_socket = 'ipc://' + ipc_socket
    core = ctx.obj.core

    logger.info('Master process PID:%s', os.getpid())

    # run hub
    core.run()


@cli_main.command('migrate')
@click.pass_context
@click.option('--dry-run', '-n', is_flag=True)
@click.option('database_url', '--database', envvar='CRCR_DATABASE')
def cli_main_migrate(ctx, dry_run, database_url):
    """DBを最新スキーマの状態にあわせる.

    :param Context ctx: Context
    :param bool dry_run: 実行しなければTrue
    :param str database_url: データベースのURL
    """
    if database_url is None:
        click.echo('Database url is not set.')
        click.echo('Please set Database url to argument `crcr migrate --database DB_URL ...`')
        click.echo('or set to environment variable `export CRCR_DATABASE=DB_URL`.')
        ctx.exit(code=-1)

    metadata = ctx.obj.metadata

    db = Database(database_url)
    db.register_message_boxes(metadata.message_boxes, metadata.schemas)

    # check meta tables
    if dry_run:
        db.check_tables()
    else:
        db.migrate()
