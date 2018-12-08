#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Bitcoin相場bot
"""

import logging
import json
import uuid

import click
import nnpy
import websocket

logger = logging.getLogger(__name__)


@click.command()
@click.option('send_to', '--to', type=click.STRING, default='ipc:///tmp/crcr_request.ipc')
@click.option('box_id', '--box-id', type=uuid.UUID, required=True)
def bitcoin_bot(send_to, box_id):
    """Bitcoinの取引をCircleCoreに送信.

    スキーマ登録: crcr schema add --name bitcoinbot address:string btc:float

    :param str send_to:
    """
    socket = nnpy.Socket(nnpy.AF_SP, nnpy.REQ)
    socket.connect(send_to)

    websocket.enableTrace(True)
    receiver = websocket.create_connection('wss://ws.blockchain.info/inv')
    receiver.send('{"op":"unconfirmed_sub"}')
    box_id = str(box_id)
    while True:
        res = json.loads(receiver.recv())
        for transaction in res['x']['out']:
            req = {
                'request': 'new_message',
                'box_id': str(box_id),
                'payload': {
                    'address': transaction['addr'],
                    'btc': transaction['value'] / 10**8,
                },
            }
            raw = json.dumps(req).encode('utf-8')
            print('send: {!r}'.format(raw))
            socket.send(raw)

            resp = socket.recv()
            print('  recv: {!r}'.format(resp))


if __name__ == '__main__':
    bitcoin_bot()
