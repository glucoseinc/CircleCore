# -*- coding: utf-8 -*-

"""CLI Main."""

from multiprocessing import Process

# community module
import click
from click.core import Context

# project module
from circle_core import server
from circle_core.server import ws, wui
from circle_core.workers import get_worker
from .context import ContextObject, ContextObjectError


@click.group()
@click.option('config_url', '--config', envvar='CRCR_CONFIG')
@click.option('crcr_uuid', '--uuid', envvar='CRCR_UUID')
@click.pass_context
def cli_main(ctx, config_url, crcr_uuid):
    """`crcr`の起点.

    :param Context ctx: Context
    :param str config_url: ConfigのURLスキーム
    :param str crcr_uuid: CircleCore UUID
    """
    if config_url is None:
        click.echo('Config is not set.')
        click.echo('Please set config to argument `crcr --config URL_SCHEME ...`')
        click.echo('or set config to environment variable `export CRCR_CONFIG=URL_SCHEME`.')
        ctx.exit(code=-1)

    if crcr_uuid is None:
        click.echo('Circle Core UUID is not set.')
        click.echo('Please set UUID to argument `crcr --uuid UUID ...`')
        click.echo('or set config to environment variable `export CRCR_UUID=UUID`.')
        ctx.exit(code=-1)

    try:
        ctx.obj = ContextObject(config_url, crcr_uuid)
    except ContextObjectError as e:
        click.echo(e)
        ctx.exit(code=-1)


@cli_main.command('env')
@click.pass_context
def cli_main_env(ctx):
    """CircleCoreの環境を表示する.

    :param Context ctx: Context
    """
    click.echo(ctx.obj.config_url)
    click.echo(ctx.obj.uuid)


@cli_main.command('run')
@click.option('--ws-port', type=click.INT, envvar='CRCR_WSPORT', default=5000)
@click.option('--ws-path', type=click.STRING, envvar='CRCR_WSPATH', default='/ws/?')
@click.option('--wui-port', type=click.INT, envvar='CRCR_WUIPORT', default=5000)
@click.option('--ipc-socket', type=click.Path(resolve_path=True), envvar='CRCR_IPCSOCK', default='/tmp/circlecore.ipc')
@click.option('workers', '--worker', type=click.STRING, envvar='CRCR_WORKERS', multiple=True)
@click.pass_obj
def cli_main_run(obj, ws_port, ws_path, wui_port, ipc_socket, workers):
    """CircleCoreの起動."""
    obj.ipc_socket = 'ipc://' + ipc_socket

    procs = [Process(target=get_worker(worker).run) for worker in workers]
    if ws_port == wui_port:
        procs.append(Process(target=server.run, args=[wui_port, obj.config]))
    else:
        app = wui.create_app(obj.config)
        procs += [
            Process(target=ws.run, args=[ws_path, ws_port]),
            Process(target=app.run, kwargs={'port': wui_port})
        ]

    for proc in procs:
        proc.daemon = True
        proc.start()

    while all(proc.is_alive() for proc in procs):
        pass

    raise ChildProcessError()
