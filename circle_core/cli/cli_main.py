# -*- coding: utf-8 -*-

"""CLI Main."""

from __future__ import absolute_import, print_function

from itertools import cycle
from multiprocessing import Process
from signal import SIGINT, signal, SIGTERM
import sys
from time import time
from uuid import UUID

# community module
import click
from click.core import Context

# project module
from circle_core import server
from circle_core.server import ws, wui
from circle_core.workers import get_worker
from .context import ContextObject, ContextObjectError
from ..database import Database


@click.group()
@click.option('metadata_url', '--metadata', envvar='CRCR_METADATA')
@click.option('crcr_uuid', '--uuid', envvar='CRCR_UUID', type=UUID)
@click.option('log_file_path', '--log-file', envvar='CRCR_LOG_FILE_PATH', default='var/log.ltsv')
@click.pass_context
def cli_main(ctx, metadata_url, crcr_uuid, log_file_path):
    """`crcr`の起点.

    :param Context ctx: Context
    :param str metadata_url: MetadataのURLスキーム
    :param str crcr_uuid: CircleCore UUID
    :param str log_file_path: ログファイルのパス
    """
    if metadata_url is None:
        click.echo('Metadata is not set.')
        click.echo('Please set metadata to argument `crcr --metadata URL_SCHEME ...`')
        click.echo('or set to environment variable `export CRCR_METADATA=URL_SCHEME`.')
        ctx.exit(code=-1)

    if crcr_uuid is None:
        click.echo('Circle Core UUID is not set.')
        click.echo('Please set UUID to argument `crcr --uuid UUID ...`')
        click.echo('or set to environment variable `export CRCR_UUID=UUID`.')
        ctx.exit(code=-1)

    try:
        ctx.obj = ContextObject(metadata_url, crcr_uuid, log_file_path)
    except ContextObjectError as e:
        click.echo(e)
        ctx.exit(code=-1)


@cli_main.command('env')
@click.pass_context
def cli_main_env(ctx):
    """CircleCoreの環境を表示する.

    :param Context ctx: Context
    """
    context_object = ctx.obj  # type: ContextObject
    click.echo(context_object.metadata_url)
    click.echo(context_object.uuid)
    click.echo(context_object.log_file_path)


@cli_main.command('run')
@click.option('--ws-port', type=click.INT, envvar='CRCR_WSPORT', default=5000)
@click.option('--ws-path', type=click.STRING, envvar='CRCR_WSPATH', default='/ws/?')
@click.option('--wui-port', type=click.INT, envvar='CRCR_WUIPORT', default=5000)
@click.option('--ipc-socket', type=click.Path(resolve_path=True), envvar='CRCR_IPCSOCK', default='/tmp/circlecore.ipc')
@click.option('workers', '--worker', type=click.STRING, envvar='CRCR_WORKERS', multiple=True)
@click.option('database_url', '--database', envvar='CRCR_DATABASE')
@click.pass_context
def cli_main_run(ctx, ws_port, ws_path, wui_port, ipc_socket, workers, database_url):
    """CircleCoreの起動."""
    ctx.obj.ipc_socket = 'ipc://' + ipc_socket
    metadata = ctx.obj.metadata
    metadata.database_url = database_url  # とりあえず...

    procs = [RestartableProcess(target=get_worker(worker).run, args=[metadata]) for worker in workers]
    if ws_port == wui_port:
        procs.append(RestartableProcess(target=server.run, args=[wui_port, metadata]))
    else:
        procs += [
            RestartableProcess(target=ws.run, args=[ws_path, ws_port]),
            RestartableProcess(target=wui.create_app(metadata).run, kwargs={'port': wui_port})
        ]

    print(
        'Websocket : ws://{host}:{port}{path}'.format(path=ws_path, port=ws_port, host='127.0.0.1'),
        file=sys.stderr)
    print('WebUI : http://127.0.0.1:{port}{path}'.format(path='/', port=ws_port), file=sys.stderr)
    print('IPC : {}'.format(ctx.obj.ipc_socket), file=sys.stderr)

    def kill_children_too(*args):
        for proc in procs:
            proc.terminate()  # 子プロセスのSIGTERMハンドラに終了時の処理を書く
        ctx.abort()
    signal(SIGTERM, kill_children_too)
    signal(SIGINT, kill_children_too)

    for proc in procs:
        proc.start()

    for proc in cycle(procs):
        if not proc.is_alive():
            click.echo('PID {} has died. Restarting...'.format(proc.pid))
            try:
                proc.start()
            except RuntimeError:
                kill_children_too()


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
    db.register_schemas_and_modules(metadata.schemas, metadata.modules)

    # check meta tables
    if dry_run:
        db.check_tables()
    else:
        db.migrate()


class RestartableProcess:
    """RestartableProcess.

    :param list args:
    :param dict kwargs:
    :param int startedTime:
    :param Process process:
    """

    def __init__(self, *args, **kwargs):
        """constructor."""
        self.args = args
        self.kwargs = kwargs
        self.startedTime = 0

    def __getattr__(self, attr):
        """delegation."""
        return getattr(self.process, attr)

    def start(self):
        """start."""
        if 10 > time() - self.startedTime:
            raise RuntimeError('Restarted process has died immediately')

        self.process = Process(*self.args, **self.kwargs)
        self.process.daemon = True
        self.process.start()
        self.startedTime = time()
