#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""一秒ごとに適当なメッセージを投げるセンサー."""

# system module
import base64
from datetime import date, datetime
import json
from time import sleep, time
import random
from uuid import UUID

# community module
import click
import nnpy


@click.command()
@click.option('send_to', '--to', type=click.STRING, default='ipc:///tmp/crcr_request.ipc')
@click.option('box_id', '--box-id', type=UUID, required=True)
@click.option('send_null_value', '--null', is_flag=True, default=False)
def many_types_bot(send_to, box_id, send_null_value):
    """一秒ごとに適当なメッセージを投げる.

    スキーマ登録: crcr schema add --name many_types int:int float:float bool:bool string:string bytes:bytes date:date datetime:datetime time:time timestamp:timestamp  # noqa
    bytes:bytes date:date datetime:datetime time:time timestamp:timestamp

    :param str send_to:
    :param UUID box_id:
    """
    def null_or_value(value):
        if send_null_value:
            return random.choice([value, None])
        return value

    socket = nnpy.Socket(nnpy.AF_SP, nnpy.REQ)
    socket.connect(send_to)

    i = 0
    while True:
        i += 1

        data = {
            'request': 'new_message',
            'box_id': str(box_id),
            'payload': {
                'int': null_or_value(i),
                'float': null_or_value(float(i)),
                'bool': null_or_value(bool(i)),
                'string': null_or_value('string_{}'.format(i)),
                'bytes': null_or_value(base64.b64encode('bytes_{}'.format(i).encode('utf-8')).decode('utf-8')),
                'date': null_or_value(str(date.today())),
                'datetime': null_or_value(str(datetime.now())),
                'time': null_or_value(str(datetime.time(datetime.now()))),
                'timestamp': null_or_value(str(datetime.fromtimestamp(time()))),
            }
        }
        msg = json.dumps(data, indent=2, ensure_ascii=False)
        socket.send(msg)

        click.echo(msg)
        sleep(1)


if __name__ == '__main__':
    many_types_bot()
