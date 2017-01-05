# -*- coding: utf-8 -*-
"""レプリケーション先からメッセージを受け取るワーカー."""
from datetime import datetime
import json
from select import select
import traceback
from uuid import UUID

from base58 import b58encode
import click
from websocket import create_connection, WebSocketConnectionClosedException

from circle_core.logger import get_stream_logger
from ..database import Database
from ..helpers.metadata import metadata
from ..helpers.nanomsg import Receiver
from ..models.message import ModuleMessage
from ..models.message_box import MessageBox
from ..models.module import Module
from ..models.schema import Schema

logger = get_stream_logger(__name__)


def get_uuid():  # テスト時には上書きする
    return click.get_current_context().obj.uuid.hex


class ReplicationSlave(object):
    def __init__(self, metadata, master_addr):
        self.ws = create_connection('ws://' + master_addr + '/replication/' + get_uuid())
        self.db = Database(metadata.database_url)
        self.metadata = metadata

    def migrate(self):
        if not metadata().writable:
            click.echo("Can't update the metadata. You must specify redis as --metadata.", err=True)
            click.get_current_context().abort()

        res = json.loads(self.ws.recv())

        schemas = [Schema(**schema) for schema in res['schemas']]
        for schema in schemas:
            metadata().register_schema(schema)

        boxes = [MessageBox(**box) for box in res['message_boxes']]
        for box in boxes:
            metadata().register_message_box(box)

        for module in res['modules']:
            metadata().register_module(Module(**module))

        self.db.register_message_boxes(boxes, schemas)
        self.db.migrate()

    def receive(self):
        dbconn = self.db._engine.connect()

        while True:
            transaction = dbconn.begin()
            try:
                try:
                    msg = ModuleMessage.decode(self.ws.recv())
                except WebSocketConnectionClosedException:
                    logger.error('WebSocket connection closed')
                    return
                logger.debug('Received from master: %r', msg)

                table = self.db.find_table_for_message(msg)
                query = table.insert().values(
                    _created_at=datetime.fromtimestamp(msg.timestamp),
                    _counter=msg.count,
                    **msg.payload
                )
                dbconn.execute(query)
            except:
                traceback.print_exc()
                transaction.rollback()
            else:
                transaction.commit()
                logger.debug('Execute query %s', query)

    def run(self):
        req = json.dumps({
            'command': 'MIGRATE'
        })
        self.ws.send(req)
        logger.debug('Send request: %s', req)
        self.migrate()

        db = Database(metadata().database_url)
        payload = {}
        for box in metadata().message_boxes:
            last_timestamp, last_count = db.last_message_identifier_for_box(box)
            payload[box.uuid.hex] = {
                'timestamp': last_timestamp,
                'count': last_count
            }

        req = json.dumps({
            'command': 'RECEIVE',
            'payload': payload
        })
        self.ws.send(req)
        logger.debug('Send request: %s', req)
        self.receive()
