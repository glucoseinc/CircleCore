# -*- coding: utf-8 -*-
"""レプリケーション先からメッセージを受け取るワーカー."""
from datetime import datetime
import json
from select import select
import traceback
from uuid import UUID

from base58 import b58encode
from click import get_current_context
from websocket import create_connection

from circle_core.logger import get_stream_logger
from ..database import Database
from ..helpers.nanomsg import Receiver
from ..models.message_box import MessageBox
from ..models.module import Module
from ..models.schema import Schema

logger = get_stream_logger(__name__)


def get_uuid():  # テスト時には上書きする
    return get_current_context().obj.uuid.hex


class Replicator(object):
    def __init__(self, metadata, master_addr):
        self.ws = create_connection('ws://' + master_addr + '/replication/' + get_uuid())
        self.db = Database(metadata.database_url)
        self.metadata = metadata

    def migrate(self):
        res = json.loads(self.ws.recv())
        boxes = [MessageBox(**box) for box in res['message_boxes']]
        schemas = [Schema(**schema) for schema in res['schemas']]
        self.db.register_message_boxes(boxes, schemas)
        self.db.migrate()

    def receive(self):
        dbconn = self.db._engine.connect()

        while True:
            transaction = dbconn.begin()
            try:
                res = json.loads(self.ws.recv())  # MessageがJSONシリアライズされたオブジェクト
                logger.debug('Received from master: %r', res)

                # TODO: MasterのModuleはmetadataに登録するべきか
                table = self.db._metadata.tables['module_' + b58encode(UUID(res['module']).bytes)]
                query = table.insert().values(
                    _created_at=datetime.fromtimestamp(res['timestamp']),
                    _counter=res['count'],
                    **res['payload']
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
        self.migrate()

        req = json.dumps({
            'command': 'RECEIVE'
        })
        self.ws.send(req)
        self.receive()
