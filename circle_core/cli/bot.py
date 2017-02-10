# -*- coding: utf-8 -*-
"""WebSocketサーバーに適当にデータを投げつけるbot."""
import json
from time import sleep
import uuid

import click
import websocket


@click.group('bot')
def cli_bot():
    """`crcr bot`の起点."""
    pass


@cli_bot.command()
@click.option('send_to', '--to', type=click.STRING, default='ws://localhost:5000/module')
@click.option('box_id', '--box-id', type=uuid.UUID, required=True)
def dummy(send_to, box_id):
    """ダミーのデータを投げる.

    スキーマ登録: crcr schema add --name dummybot count:int body:text

    :param str send_to:
    """
    websocket.enableTrace(True)
    ws = websocket.create_connection(send_to)
    box_id = str(box_id)

    i = 0
    while True:
        i += 1
        d = {'count': i, 'body': "Greetings from a bot", '_box': box_id}
        ws.send(json.dumps(d, indent=2, ensure_ascii=False))
        click.echo('I sent a message {} times'.format(i))
        sleep(1)


@cli_bot.command()
@click.option('send_to', '--to', type=click.STRING, default='ws://localhost:5000/module')
@click.option('box_id', '--box-id', type=uuid.UUID, required=True)
def bitcoin(send_to, box_id):
    """Bitcoinの取引をCircleCoreに送信.

    スキーマ登録: crcr schema add --name bitcoinbot address:text btc:float

    :param str send_to:
    """
    websocket.enableTrace(True)
    sender = websocket.create_connection(send_to)
    receiver = websocket.create_connection('wss://ws.blockchain.info/inv')
    receiver.send('{"op":"unconfirmed_sub"}')
    box_id = str(box_id)
    while True:
        res = json.loads(receiver.recv())
        for transaction in res['x']['out']:
            req = json.dumps({
                'address': transaction['addr'],
                'btc': transaction['value'] / 10 ** 8,
                '_box': box_id,
            })
            sender.send(req)
