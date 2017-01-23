# -*- coding: utf-8 -*-
"""センサデータを受け取って保存する"""

# system module
from datetime import datetime
import time
from uuid import UUID

from six import PY3

# project module
from circle_core.logger import get_stream_logger
from ..database import Database
from ..exceptions import ModuleNotFoundError, SchemaNotFoundError
from ..helpers.nanomsg import Receiver
from ..helpers.topics import ModuleMessageTopic
from ..models.metadata import MetadataIniFile, MetadataRedis
from ..timed_db import TimedDBBundle

if PY3:
    from typing import Tuple, Union


logger = get_stream_logger(__name__)


def run(metadata):
    """clickから起動される.
    """
    DataReceiver(metadata).run()


class DataReceiver(object):
    def __init__(self, metadata, cycle_time=1.0, cycle_count=10):
        self.metadata = metadata

        # commitする、メッセージ数と時間
        self.cycle_count = cycle_count
        self.cycle_time = cycle_time

        self.message_receiver = Receiver(ModuleMessageTopic())
        self.message_receiver.set_timeout(int(self.cycle_time * 1000))

        self.db = Database(metadata.database_url)
        self.db.register_message_boxes(metadata.message_boxes, metadata.schemas)

        self.time_db_bundle = TimedDBBundle(metadata.prefix)

        if not self.db.diff_database().is_ok:
            # TODO: 例外処理
            raise Exception

        self.conn = self.db._engine.connect()
        self.transaction = None

    def run(self):
        self.begin_transaction()

        while True:
            for msg in self.message_receiver.incoming_messages():
                logger.debug('received a module data for %s-%s : %r', msg.module_uuid, msg.box_id, msg.payload)

                self.store_message(msg)

                if self.should_commit():
                    self.commit_transaction()
                    self.begin_transaction()

            if self.should_commit():
                self.commit_transaction()
                self.begin_transaction()

        if self.write_count:
            self.commit_transaction()

    def begin_transaction(self):
        self.transaction = self.conn.begin()
        self.write_count, self.transaction_begin = 0, time.time()

        # timed dbのアップデート用にlist((box_id, timestamp))を記録する
        self.updates = []

    def commit_transaction(self):
        logger.debug('commit data count=%d', self.write_count)
        self.transaction.commit()
        # TODO: timeddbには1秒前のデータのみ入れる
        self.time_db_bundle.update(self.updates)
        self.updates = self.transaction = self.write_count = self.transaction_begin = None

    def rollback_transaction(self):
        self.transaction.rollback()
        self.updates = self.transaction = self.write_count = self.transaction_begin = None

    def should_commit(self):
        return (
            self.write_count and
            self.transaction_begin and
            (self.write_count >= self.cycle_count or (time.time() - self.transaction_begin) >= self.cycle_time)
        )

    def store_message(self, msg):
        assert self.transaction is not None

        table = self.db.find_table_for_message_box(msg.box_id)
        query = table.insert().values(
            _created_at=msg.timestamp,
            _counter=msg.count,
            **msg.payload
        )
        self.conn.execute(query)
        self.write_count += 1

        assert isinstance(msg.box_id, UUID)
        self.updates.append((msg.box_id, msg.timestamp))
