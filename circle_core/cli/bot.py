# -*- coding: utf-8 -*-
"""WebSocketサーバーに適当にデータを投げつけるbot."""
import json
from time import sleep

import click
import websocket


@click.group('bot')
def cli_bot():
    """`crcr bot`の起点."""
    pass


@cli_bot.command()
@click.option('addr', '--ws-addr', type=click.STRING, envvar='CRCR_WSADDR', default='ws://localhost:5000/ws')
def run(addr):
    """botの起動."""
    websocket.enableTrace(True)
    ws = websocket.create_connection(addr)
    i = 0
    while True:
        i += 1
        ws.send(json.dumps({'count': i, 'body': "Greetings from a bot"}, indent=2, ensure_ascii=False))
        click.echo('I sent a message {} times'.format(i))
        sleep(1)
