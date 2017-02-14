# -*- coding: utf-8 -*-
"""センサデータを受け取って保存するCircleModule"""

# system module
from collections import defaultdict
from datetime import datetime
import logging
import math
import threading
import time
from uuid import UUID

from six import PY3

# project module
from circle_core.constants import RequestType
from .base import CircleWorker, register_worker_factory
from ..core.message import ModuleMessage
from ..core.metadata_event_listener import MetaDataEventListener
from ..database import Database
from ..exceptions import MessageBoxNotFoundError, ModuleNotFoundError, SchemaNotFoundError
from ..helpers.topics import make_message_topic
from ..models import MessageBox, NoResultFound, Schema
from ..timed_db import TimedDBBundle


logger = logging.getLogger(__name__)
WORKER_DATARECEIVER = 'datareceiver'


@register_worker_factory(WORKER_DATARECEIVER)
def create_http_worker(core, type, key, config):
    assert type == WORKER_DATARECEIVER
    defaults = {
        'cyclce_time': '5.0',
        'cycle_count': '100',
    }
    return DataReceiverWorker(
        core, key,
        db_url=config.get('db'),
        time_db_dir=config.get('time_db_dir'),
        cycle_time=config.getfloat('cyclce_time', vars=defaults),
        cycle_count=config.getint('cycle_count', vars=defaults),
    )


class DataReceiverWorker(CircleWorker):
    """
    request_socketに届いた、生のメッセージのスキーマをチェックしたあと、プライマリキーを付与してDBに保存する。
    また、同時にhubにも流す。
    """
    worker_type = WORKER_DATARECEIVER

    def __init__(self, core, key, db_url, time_db_dir, cycle_time=1.0, cycle_count=10):
        super(DataReceiverWorker, self).__init__(core, key)

        # commitする、メッセージ数と時間
        self.cycle_count = cycle_count
        self.cycle_time = cycle_time

        self.db = Database(db_url)
        self.writer = self.db.make_writer(cycle_time=cycle_time, cycle_count=cycle_count)
        self.writer.on_commit_transaction = self.on_commit

        self.time_db_bundle = TimedDBBundle(time_db_dir)
        # timed dbのアップデート用にlist((box_id, timestamp))を記録する
        self.updates = []

        self.counter_lock = threading.Lock()

        # metadataに関するイベントを監視する
        self.listener = MetaDataEventListener()
        self.listener.on('messagebox', 'after', self.on_change_messagebox)

        # messageに関するイベントを監視する
        self.core.hub.register_handler(RequestType.NEW_MESSAGE.value, self.on_new_message)

    def initialize(self):
        """override"""
        # start
        self.counters = defaultdict(int)

    def finalize(self):
        """override"""
        self.writer.commit()

        # flush all updates
        self.time_db_bundle.update(self.updates)
        self.updates = []

    def on_new_message(self, request):
        """新しいメッセージを受けとった"""
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

        return response

    def on_change_messagebox(self, what, target):
        """metadataのmessageboxが更新されたら呼ばれる"""
        if what == 'after_delete':
            # message boxが削除されたので消す
            self.writer.commit()
            self.db.drop_message_box(target, connection=self.conn)

    def find_message_box(self, box_id):
        # DBに直接触っちゃう
        try:
            box = MessageBox.query.filter_by(uuid=box_id).one()
        except NoResultFound:
            raise MessageBoxNotFoundError(box_id)

        return box

    def store_message(self, message_box, payload):
        # make primary key
        msg = self.make_primary_key(message_box, payload)
        self.writer.store(message_box, msg)

        self.updates.append((msg.box_id, msg.timestamp))

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

    def on_commit(self, writer):
        """DBにコミットするタイミングで時系列DBも更新する"""
        # 現在の秒のデータは更新中なので、その手前までを保存する...
        threshold = math.floor(time.time()) - 1
        for idx, (box_id, timestamp) in enumerate(self.updates):
            if timestamp >= threshold:
                break
        updates, self.updates = self.updates[:idx], self.updates[idx:]
        self.time_db_bundle.update(updates)
