# -*- coding: utf-8 -*-
"""センサデータを受け取って保存するCircleModule"""

# system module
from collections import defaultdict
from datetime import datetime
import logging
import time
import threading
from uuid import UUID

from six import PY3

# project module
from circle_core.constants import RequestType
from ..database import Database
from ..exceptions import MessageBoxNotFoundError, ModuleNotFoundError, SchemaNotFoundError
from ..timed_db import TimedDBBundle
from ..models import Schema, MessageBox, NoResultFound
from ..models.message import ModuleMessage
from ..helpers.topics import make_message_topic
from .base import CircleWorker, register_worker_factory


logger = logging.getLogger(__name__)
WORKER_DATARECEIVER = 'datareceiver'


class DataReceiverWorker(CircleWorker):
    """
    request_socketに届いた、生のメッセージのスキーマをチェックしたあと、プライマリキーを付与してDBに保存する。
    また、同時にhubにも流す。
    """

    @classmethod
    def create(cls, core, type, key, config):
        assert type == WORKER_DATARECEIVER
        defaults = {
            'cyclce_time': '1.0',
            'cycle_count': '10',
        }
        return cls(
            core,
            db_url=config.get('db'),
            time_db_dir=config.get('time_db_dir'),
            cycle_time=config.getfloat('cyclce_time', vars=defaults),
            cycle_count=config.getint('cycle_count', vars=defaults),
        )

    def __init__(self, core, db_url, time_db_dir, cycle_time=1.0, cycle_count=10):
        super(DataReceiverWorker, self).__init__(core)

        # commitする、メッセージ数と時間
        self.cycle_count = cycle_count
        self.cycle_time = cycle_time

        self.db = Database(db_url)
        # self.db.register_message_boxes(MessageBox.query.all(), Schema.query.all())
        self.time_db_bundle = TimedDBBundle(time_db_dir)

        # if not self.db.diff_database().is_ok:
        #     # TODO: 例外処理
        #     raise Exception

        self.conn = self.db._engine.connect()
        self.transaction = None
        self.counter_lock = threading.Lock()

        self.core.hub.register_handler(RequestType.NEW_MESSAGE.value, self.on_new_message)

    def initialize(self):
        # start
        self.begin_transaction()
        self.counters = defaultdict(int)

    def finalize(self):
        if self.write_count:
            self.commit_transaction()

    def on_new_message(self, request):
        box_id = request['box_id']
        payload = request['payload']

        try:
            message_box = self.find_message_box(box_id)
        except MessageBoxNotFoundError:
            return {'response': 'failed', 'message': 'message box not found'}

        if not message_box.schema.check_match(payload):
            # TODO: save error log
            return {'response': 'failed', 'message': 'schema not match'}

        msg = self.store_message(message_box, payload)
        message = msg.to_json()
        response = {'response': 'message_accepted', 'message': message}

        # pusblish
        self.core.hub.publish(
            make_message_topic(message_box.module.uuid, message_box.uuid),
            message
        )

        if self.should_commit():
            self.commit_transaction()
            self.begin_transaction()

        return response

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

    def find_message_box(self, box_id):
        # DBに直接触っちゃう
        try:
            box = MessageBox.query.filter_by(uuid=box_id).one()
        except NoResultFound:
            raise MessageBoxNotFoundError(box_id)

        return box

    def store_message(self, message_box, payload):
        assert self.transaction is not None

        # make primary key
        msg = self.make_primary_key(message_box, payload)
        self.db.store_message(message_box, msg, connection=self.conn)
        self.write_count += 1

        self.updates.append((message_box.uuid, msg.timestamp))

        return msg

    def make_primary_key(self, message_box, payload):
        timestamp = ModuleMessage.make_timestamp()
        with self.counter_lock:
            counter = self.counters[message_box.uuid]
            if counter >= 32767:
                counter = 1
            else:
                counter += 1
            self.counters[message_box.uuid] = counter

        return ModuleMessage(message_box.uuid, timestamp, counter, payload)


register_worker_factory(
    WORKER_DATARECEIVER,
    DataReceiverWorker.create,
)
