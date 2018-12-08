#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
CircleCoreの九大人流センサーのbot
"""

import logging
import json
import uuid

import click
import nnpy
import websocket

logger = logging.getLogger(__name__)


@click.command()
@click.option('receive_from', '--from', type=click.STRING, default='ws://api.coi.bodic.org/websocket')
@click.option('send_to', '--to', type=click.STRING, default='ipc:///tmp/crcr_request.ipc')
@click.option('box_id', '--box-id', type=uuid.UUID, required=True)
def echo_bot(receive_from, send_to, box_id):
    socket = nnpy.Socket(nnpy.AF_SP, nnpy.REQ)
    socket.connect(send_to)

    websocket.enableTrace(True)
    receiver = websocket.create_connection(receive_from)

    while True:
        receiver = websocket.create_connection(receive_from, timeout=10)

        i = 0
        while True:
            i += 1
            try:
                msg = receiver.recv()
            except websocket.WebSocketTimeoutException:
                logger.error("I'm not received new messages anymore. Reconnecting...")
                break

            for j, dic in enumerate(json.loads(msg)):
                req = {
                    'request': 'new_message',
                    'box_id': str(box_id),
                    'payload': dic,
                }
                raw = json.dumps(req).encode('utf-8')
                print('send: {!r}'.format(raw))
                socket.send(raw)

                resp = socket.recv()
                print('  recv: {!r}'.format(resp))


if __name__ == '__main__':
    echo_bot()
