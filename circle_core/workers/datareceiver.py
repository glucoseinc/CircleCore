# -*- coding: utf-8 -*-
"""センサデータを受け取って保存するCircleModule"""

# system module
import asyncio
import logging
import threading
import typing
from collections import defaultdict

# project module
from circle_core.constants import RequestType
from circle_core.message import ModuleMessage

from .base import CircleWorker, WorkerType, register_worker_factory
from ..core.metadata_event_listener import MetaDataEventListener
from ..database import Database
from ..exceptions import MessageBoxNotFoundError
from ..helpers.topics import make_message_topic
from ..models import MessageBox, NoResultFound

logger = logging.getLogger(__name__)
WORKER_DATARECEIVER = typing.cast(WorkerType, 'datareceiver')


@register_worker_factory(WORKER_DATARECEIVER)
def create_datareceiver_worker(core, type, key, config):
    assert type == WORKER_DATARECEIVER
    defaults = {
        'cycle_time': '2.0',
        'cycle_count': '100',
    }
    return DataReceiverWorker(
        core,
        key,
        db_url=config.get('db'),
        time_db_dir=config.get('time_db_dir'),
        log_dir=config.get('log_dir'),
        cycle_time=config.getfloat('cycle_time', vars=defaults),
        cycle_count=config.getint('cycle_count', vars=defaults),
    )


class DataReceiverWorker(CircleWorker):
    """
    request_socketに届いた、生のメッセージのスキーマをチェックしたあと、プライマリキーを付与してDBに保存する。
    また、同時にhubにも流す。
    """
    worker_type = WORKER_DATARECEIVER

    def __init__(self, core, key, db_url, time_db_dir, log_dir, cycle_time=1.0, cycle_count=10):
        super(DataReceiverWorker, self).__init__(core, key)

        # commitする、メッセージ数と時間
        self.cycle_count = cycle_count
        self.cycle_time = cycle_time

        self.db = Database(db_url, time_db_dir, log_dir)
        self.writer = self.db.make_writer(cycle_time=cycle_time, cycle_count=cycle_count)

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
        asyncio.get_event_loop().run_until_complete(self.writer.flush(flush_all=True))

    async def on_new_message(self, request):
        """nanomsgから新しいメッセージを受けとった"""
        box_id = request['box_id']
        payload = request['payload']

        await self.receive_new_message(box_id, payload)

    async def receive_new_message(self, box_id, payload):
        try:
            message_box = self.find_message_box(box_id)
        except MessageBoxNotFoundError:
            return {'response': 'failed', 'message': 'message box not found'}

        if not message_box.schema.check_match(payload):
            logger.warning(
                'box {box_id} : message not matching schema was received. '
                'expected {expected}, received {received}'.format(
                    box_id=box_id, expected=message_box.schema.properties, received=payload
                )
            )
            return {'response': 'failed', 'message': 'schema not match'}

        msg = await self.store_message(message_box, payload)
        message = msg.to_json()
        response = {'response': 'message_accepted', 'message': message}

        # publish
        logger.debug('publish new message: %s', message)
        self.core.hub.publish(make_message_topic(message_box.module.uuid, message_box.uuid), message)

        return response

    def on_change_messagebox(self, what, target):
        """metadataのmessageboxが更新されたら呼ばれる"""
        if what == 'after_delete':
            if asyncio.get_event_loop().is_running():
                logger.error('current loop is running')
                asyncio.ensure_future(self.writer.flush())
            else:
                asyncio.get_event_loop().run_until_complete(self.writer.flush)

    def find_message_box(self, box_id):
        # DBに直接触っちゃう
        try:
            box = MessageBox.query.filter_by(uuid=box_id).one()
        except NoResultFound:
            raise MessageBoxNotFoundError(box_id)

        return box

    async def store_message(self, message_box, payload):
        # make primary key
        msg = self.make_primary_key(message_box, payload)
        await self.writer.store(message_box, msg)

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
