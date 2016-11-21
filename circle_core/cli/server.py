"""CLI Server."""
import click
from circle_core import server


@click.group('server')
def cli_server():
    """`crcr server`の起点."""
    pass


@cli_server.command()
def run():
    """サーバーの起動."""
    click.echo('Tornado and Flask are running')
    server.run()
