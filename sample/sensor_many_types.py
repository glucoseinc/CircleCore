#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""一秒ごとに適当なメッセージを投げるセンサー."""

# system module
import base64
import json
from time import sleep, time
from uuid import UUID
from datetime import date, datetime

# community module
import click
import nnpy


@click.command()
@click.option('send_to', '--to', type=click.STRING, default='ipc:///tmp/crcr_request.ipc')
@click.option('box_id', '--box-id', type=UUID, required=True)
def many_types_bot(send_to, box_id):
    """一秒ごとに適当なメッセージを投げる.

    スキーマ登録: crcr schema add --name many_types int:int float:float bool:bool string:string
    bytes:bytes date:date datetime:datetime time:time timestamp:timestamp

    :param str send_to:
    :param UUID box_id:
    """
    socket = nnpy.Socket(nnpy.AF_SP, nnpy.REQ)
    socket.connect(send_to)

    i = 0
    while True:
        i += 1

        data = {
            'request': 'new_message',
            'box_id': str(box_id),
            'payload': {
                'int': i,
                'float': float(i),
                'bool': bool(i),
                'string': 'string_{}'.format(i),
                'bytes': base64.b64encode('bytes_{}'.format(i).encode('utf-8')).decode('utf-8'),
                'date': str(date.today()),
                'datetime': str(datetime.now()),
                'time': str(datetime.time(datetime.now())),
                'timestamp': str(datetime.fromtimestamp(time())),
            }
        }
        msg = json.dumps(data, indent=2, ensure_ascii=False)
        socket.send(msg)

        click.echo(msg)
        sleep(1)


if __name__ == '__main__':
    many_types_bot()
