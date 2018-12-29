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
@click.option('interval', '--interval', type=float, default=1.0)
@click.option('silent', '--silent', is_flag=True)
def counter_bot(send_to, box_id, interval=1.0, silent=False):
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

        msg = json.dumps(
            {
                'request': 'new_message',
                'box_id': str(box_id),
                'payload': {
                    'count': i,
                    'body': "Greetings from a bot",
                }
            },
            indent=2,
            ensure_ascii=False
        )
        socket.send(msg)

        if not silent:
            click.echo('I sent a message {} times'.format(i))
        sleep(interval)


if __name__ == '__main__':
    counter_bot()
