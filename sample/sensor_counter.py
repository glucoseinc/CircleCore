# -*- coding: utf-8 -*-
"""一秒ごとに適当なメッセージを投げるセンサー."""
import json
from time import sleep
from uuid import UUID

import click
import nnpy


@click.command()
@click.option('send_to', '--to', type=click.STRING, default='ipc:///tmp/crcr_request.ipc')
@click.option('box_id', '--box-id', type=UUID, required=True)
def counter_bot(send_to, box_id):
    """一秒ごとに適当なメッセージを投げる.

    スキーマ登録: crcr schema add --name counterbot count:int body:string

    :param str send_to:
    :param UUID box_id:
    """
    socket = nnpy.Socket(nnpy.AF_SP, nnpy.REQ)
    socket.connect(send_to)

    i = 0
    while True:
        i += 1

        msg = json.dumps({
            'request': 'new_message',
            'box_id': str(box_id),
            'payload': {
                'count': i,
                'body': "a" * 512,
            }
        }, indent=2, ensure_ascii=False)
        socket.send(msg)

        click.echo('I sent a message {} times'.format(i))
        sleep(1)


if __name__ == '__main__':
    counter_bot()
