# -*- coding: utf-8 -*-
"""WebSocketサーバーに適当にデータを投げつけるbot."""
import json
from time import sleep

import click
import websocket

from ..logger import get_stream_logger


logger = get_stream_logger()


@click.group('bot')
def cli_bot():
    """`crcr bot`の起点."""
    pass


@cli_bot.command()
@click.option('receive_from', '--from', type=click.STRING, default='ws://api.coi.bodic.org/websocket')
@click.option('send_to', '--to', type=click.STRING, default='ws://localhost:5000/module')
def echo(receive_from, send_to):
    """--fromから--toへメッセージをたらい回し.

    :param str receive_from:
    :param str send_to:
    """
    websocket.enableTrace(True)
    sender = websocket.create_connection(send_to)

    while True:
        receiver = websocket.create_connection(receive_from, timeout=10)

        i = 0
        while True:
            i += 1
            try:
                msg = receiver.recv()
            except websocket.WebSocketTimeoutException:
                logger.error("I'm no longer received new messages anymore. Reconnecting...")
                break

            for dic in json.loads(msg):
                sender.send(json.dumps(dic))


@cli_bot.command()
@click.option('send_to', '--to', type=click.STRING, default='ws://localhost:5000/module')
def dummy(send_to):
    """ダミーのデータを投げる.

    :param str send_to:
    """
    websocket.enableTrace(True)
    ws = websocket.create_connection(send_to)
    i = 0
    while True:
        i += 1
        ws.send(json.dumps({'count': i, 'body': "Greetings from a bot"}, indent=2, ensure_ascii=False))
        click.echo('I sent a message {} times'.format(i))
        sleep(1)
