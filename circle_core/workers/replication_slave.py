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

from circle_core.exceptions import MigrationError
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
    def __init__(self, metadata, master_addr, module_uuids):
        self.ws = create_connection('ws://' + master_addr + '/replication/' + get_uuid())
        self.db = Database(metadata.database_url)
        self.metadata = metadata
        self.module_uuids = module_uuids

    def migrate(self):
        if not metadata().writable:
            click.echo("Can't update the metadata. You must specify redis as --metadata.", err=True)
            click.get_current_context().abort()

        res = json.loads(self.ws.recv())

        schemas = [Schema(**schema) for schema in res['schemas']]
        for schema in schemas:
            metadata().register_schema(schema)

        boxes = [MessageBox(of_master=True, **box) for box in res['message_boxes']]
        for box in boxes:
            metadata().register_message_box(box)

        modules = [Module(**module) for module in res['modules']]  # FIXME: message_box_uuidsをlist化する
        for module in modules:
            metadata().register_module(module)

        self.db.register_message_boxes(boxes, schemas)
        try:
            self.db.migrate()
        except MigrationError:
            click.echo("A schema of the master's module was changed", err=True)
            click.get_current_context().abort()
            raise

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
                    _created_at=msg.timestamp,
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
            'command': 'MIGRATE',
            'module_uuids': self.module_uuids
        })
        self.ws.send(req)
        logger.debug('Send request: %s', req)
        self.migrate()

        db = Database(metadata().database_url)
        payload = {}
        for module_uuid in self.module_uuids:
            module = metadata().find_module(module_uuid)
            for box_uuid in module.message_box_uuids:
                box = metadata().find_message_box(box_uuid)
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
