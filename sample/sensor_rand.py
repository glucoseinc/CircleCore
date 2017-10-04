#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
CircleCoreの九大人流センサーのbot
"""

import datetime
import logging
import json
import random
import time
import uuid

import click
import nnpy


logger = logging.getLogger(__name__)


@click.command()
@click.option('send_to', '--to', type=click.STRING, default='ipc:///tmp/crcr_request.ipc')
@click.option('box_id', '--box-id', type=uuid.UUID, required=True)
def rand_bot(send_to, box_id):
    """ダミーのデータを投げる.

    スキーマ登録: crcr schema add --name dummybot count:int body:text

    :param str send_to:
    """
    socket = nnpy.Socket(nnpy.AF_SP, nnpy.REQ)
    socket.connect(send_to)
    box_id = str(box_id)
    i = 0
    while True:
        i += 1
        req = {
            'request': 'new_message',
            'box_id': box_id,
            'payload': {
                # 'count': i,
                'at': datetime.datetime.utcnow().isoformat('T'),
                'value': random.randint(-32768, 32767),
            }
        }
        raw = json.dumps(req).encode('utf-8')
        click.echo('send: {!r}'.format(raw))
        socket.send(raw)

        resp = socket.recv()
        click.echo('  recv: {!r}'.format(resp))

        time.sleep(random.randint(1, 100) / 1000.0)


if __name__ == '__main__':
    rand_bot()
