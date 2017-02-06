# -*- coding: utf-8 -*-
"""センサデータを受け取って保存するCircleModule"""

# system module
from datetime import datetime
import logging
import time
from uuid import UUID

from six import PY3

# project module
from ..database import Database
from ..exceptions import ModuleNotFoundError, SchemaNotFoundError
from ..helpers.nanomsg import Receiver
from ..helpers.topics import ModuleMessageTopic
from ..timed_db import TimedDBBundle
from ..models import Schema, MessageBox
from .base import CircleWorker, register_worker_factory


logger = logging.getLogger(__name__)
WORKER_DATARECEIVER = 'datareceiver'


class DataReceiverWorker(CircleWorker):
    @classmethod
    def create(cls, core, type, key, config):
        assert type == WORKER_DATARECEIVER
        defaults = {
            'hub': '${circle_core:hub}',
            'cyclce_time': '1.0',
            'cycle_count': '10',
        }
        return cls(
            core,
            db_url=config.get('db'),
            time_db_dir=config.get('time_db_dir'),
            hub=config.get('hub', vars=defaults),
            cycle_time=config.getfloat('cyclce_time', vars=defaults),
            cycle_count=config.getint('cycle_count', vars=defaults),
        )

    def __init__(self, core, db_url, hub, time_db_dir, cycle_time=1.0, cycle_count=10):
        super(DataReceiverWorker, self).__init__(core)

        # commitする、メッセージ数と時間
        self.cycle_count = cycle_count
        self.cycle_time = cycle_time

        self.message_receiver = Receiver(hub, ModuleMessageTopic())
        self.message_receiver.set_timeout(int(self.cycle_time * 1000))

        self.db = Database(db_url)
        self.db.register_message_boxes(MessageBox.query.all(), Schema.query.all())
        self.time_db_bundle = TimedDBBundle(time_db_dir)

        if not self.db.diff_database().is_ok:
            # TODO: 例外処理
            raise Exception

        self.conn = self.db._engine.connect()
        self.transaction = None

    def run(self):
        logger.info('DataReceiver running...')
        self.begin_transaction()

        while True:
            print('hogehoge')
            for msg in self.message_receiver:
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


register_worker_factory(
    WORKER_DATARECEIVER,
    DataReceiverWorker.create,
)
