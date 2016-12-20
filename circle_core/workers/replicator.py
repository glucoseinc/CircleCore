# -*- coding: utf-8 -*-
"""レプリケーション先からメッセージを受け取るワーカー."""
import json
from select import select

from click import get_current_context
from websocket import create_connection

from circle_core.logger import get_stream_logger
from ..database import Database
from ..helpers.nanomsg import Receiver
from ..models.module import Module
from ..models.schema import Schema

logger = get_stream_logger(__name__)


def get_uuid():  # テスト時には上書きする
    return get_current_context().obj.uuid.hex


def run(metadata, master_addr):
    """`crcr run`の下で走る."""
    db = Database(metadata.database_url)
    conn = create_connection('ws://' + master_addr + '/replication/' + get_uuid())
    req = json.dumps({
        'command': 'MIGRATE'
    })
    conn.send(req)
    res = json.loads(conn.recv())
    modules = [Module(**module) for module in res['modules']]
    schemas = [Schema(**schema) for schema in res['schemas']]
    db.register_schemas_and_modules(schemas, modules)
    db.migrate()

    req = json.dumps({
        'command': 'RETRIEVE'
    })
    conn.send(req)
