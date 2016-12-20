# -*- coding: utf-8 -*-
"""CLI Replication."""
import json

import click
from tornado.gen import coroutine
from tornado.ioloop import IOLoop
from websocket import create_connection

from ..database import Database
from ..models.module import Module
from ..models.schema import Schema


@click.group('replication')
def cli_replication():
    """`crcr replication`の起点."""
    pass


@cli_replication.command('add')
@click.argument('master_addr')
@click.option('database_url', '--database', envvar='CRCR_DATABASE')  # トップレベルの引数にしたほうが良いのでは
@click.pass_obj
def replication_add(obj, master_addr, database_url):
    """別のCircleCoreとの同期を開始.

    DBのマイグレーション
    TODO: Redisかどこかに現在の同期先の情報を保存

    :param str master_addr:
    """
    db = Database(database_url)
    conn = create_connection('ws://' + master_addr + '/replication/' + obj.uuid.hex)
    req = json.dumps({
        'command': 'MIGRATE'
    })
    conn.send(req)
    res = json.loads(conn.recv())
    modules = [Module(**module) for module in res['modules']]
    schemas = [Schema(**schema) for schema in res['schemas']]
    db.register_schemas_and_modules(schemas, modules)
    db.migrate()
