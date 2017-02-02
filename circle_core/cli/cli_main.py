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
from circle_core import server
from circle_core.core import CircleCore
from circle_core.server import ws, wui
from circle_core.workers import datareceiver
from circle_core.workers.replication_slave import ReplicationSlave
from .context import CLIContextObject
from .utils import generate_uuid, RestartableProcess
from ..database import Database
from ..models import CcInfo, MetadataError


@click.group()
@click.option('config_file_path', '--config', '-c', type=click.Path())
# @click.option('metadata_url', '--metadata', envvar='CRCR_METADATA')
# @click.option('log_file_path', '--log-file', envvar='CRCR_LOG_FILE_PATH', default='var/log.ltsv')
@click.pass_context
def cli_main(ctx, config_file_path):
    """`crcr`の起点.

    :param Context ctx: Context
    :param str config_file_path: iniファイルのpath
    """
    # initialize console logging
    _init_logging()

    if config_file_path:
        core = CircleCore.load_from_config(config_file_path)
    else:
        core = CircleCore.load_from_default_config_file()

    ctx.obj = CLIContextObject(core)


def _init_logging():
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
        root_logger.setLevel(logging.DEBUG)


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
@click.option('--ws-port', type=click.INT, envvar='CRCR_WSPORT', default=5000)
@click.option('--ws-path', type=click.STRING, envvar='CRCR_WSPATH', default='/module/?')
@click.option('--wui-port', type=click.INT, envvar='CRCR_WUIPORT', default=5000)
@click.option('--ipc-socket', type=click.Path(resolve_path=True), envvar='CRCR_IPCSOCK', default='/tmp/circlecore.ipc')
@click.option('replicate_from', '--replicate', type=click.STRING, envvar='CRCR_REPLICATION', multiple=True,
              help='module_uuid@hostname:port', callback=validate_replication_master_addr)
@click.option('database_url', '--database', envvar='CRCR_DATABASE')
@click.option('--prefix', envvar='CRCR_PREFIX', default=lambda: os.getcwd())
@click.option('--debug', is_flag=True)
@click.pass_context
def cli_main_run(ctx, ws_port, ws_path, wui_port, ipc_socket, replicate_from, database_url, prefix, debug):
    """CircleCoreの起動."""
    ctx.obj.ipc_socket = 'ipc://' + ipc_socket
    metadata = ctx.obj.metadata
    metadata.database_url = database_url  # とりあえず...
    metadata.prefix = prefix  # とりあえず...

    for addr, value in groupby([module_and_addr.split('@') for module_and_addr in replicate_from], lambda x: x[1]):
        modules = [module_and_addr[0] for module_and_addr in value]
        RestartableProcess(target=lambda: ReplicationSlave(metadata, addr, modules).run()).start()

    RestartableProcess(target=datareceiver.run, args=[metadata]).start()

    if ws_port == wui_port:
        RestartableProcess(target=server.run, args=[wui_port, metadata, debug]).start()
    else:
        RestartableProcess(target=ws.run, args=[metadata, ws_path, ws_port]).start()
        RestartableProcess(target=wui.create_app(metadata).run, kwargs={'port': wui_port}).start()

    click.echo('Websocket : ws://{host}:{port}{path}'.format(path=ws_path, port=ws_port, host='127.0.0.1'), err=True)
    click.echo('WebUI : http://127.0.0.1:{port}{path}'.format(path='/', port=ws_port), err=True)
    click.echo('IPC : {}'.format(ctx.obj.ipc_socket), err=True)

    RestartableProcess.wait_all()


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
