#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
受信したメッセージを標準出力に表示するSubscriber.
"""

import click
import nnpy


@click.command()
@click.option('receive_from', '--from', type=click.STRING, default='ipc:///tmp/crcr_hub.ipc',
              help='Set hub socket. (see circle_core.ini "hub_socket")')
@click.option('--topic', type=click.STRING,
              help='Filter receiving message.')
@click.option('--timeout', type=click.INT,
              help='Set timeout. (unit: sec.)')
def subscribe(receive_from, topic, timeout):
    socket = nnpy.Socket(nnpy.AF_SP, nnpy.SUB)
    socket.connect(receive_from)

    socket.setsockopt(nnpy.SUB, nnpy.SUB_SUBSCRIBE, topic or '')
    if timeout:
        socket.setsockopt(nnpy.SOL_SOCKET, nnpy.RCVTIMEO, timeout * 1000)

    while True:
        try:
            raw = socket.recv()
            message = raw.decode('utf-8')
            click.echo(message)
        except nnpy.NNError as e:
            click.echo(e)
            break
    socket.close()


if __name__ == '__main__':
    subscribe()
