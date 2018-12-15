import datetime
import math
import time
from concurrent.futures import ThreadPoolExecutor
from typing import TYPE_CHECKING

import sqlalchemy.exc
import tornado.ioloop
from tornado.concurrent import run_on_executor
# from tornado.locks import Lock

from .base import DBWriter
from ..exceptions import DatabaseWriteFailed
from ..logger import logger
from ..message import ModuleMessage
from ..timed_db import TimedDBBundle

if TYPE_CHECKING:
    from tornado.ioloop import _Timeout

    from ..models import MessageBox


class QueuedDBWriter(DBWriter):
    """QueuedWriter.
    TODO: Fill blank

    :param Database database:
    :param TimedDBBundle time_db_bundle:
    :param List updates:  TimeDBに書き込むためのデータを持っている
    :param float cycle_count:
    :param int cycle_time:
    :param Connection connection:
    :param Optional[_Timeout] timeout:
    """
    # database周りのexecution
    executor = ThreadPoolExecutor(2)

    def __init__(self, database, time_db_dir, cycle_time=10.0, cycle_count=100):
        """init.
        TODO: Fill blank

        :param Database database:
        :param str time_db_dir:
        :param float cycle_time:
        :param int cycle_count:
        """
        if cycle_time < 0:
            raise ValueError
        if cycle_count < 0:
            raise ValueError

        self.loop = tornado.ioloop.IOLoop.current()
        # self.updates_lock = Lock()

        # RDB
        self.database = database
        # 時系列DB
        self.time_db_bundle = TimedDBBundle(time_db_dir)
        # timed dbのアップデート用にlist((box_id, timestamp))を記録する
        self.updates = []

        self.cycle_count = cycle_count
        self.cycle_time = datetime.timedelta(seconds=cycle_time)

        self.connection = None
        self.timeout = None

        # 接続再試行
        self.retry_connect = None

    # override
    async def store(self, message_box: 'MessageBox', message: ModuleMessage) -> bool:
        """store.
        TODO: Fill blank

        storeはシリアライズされているんだっけ???
        """

        if not self.timeout:
            self.write_count = 0
            self.timeout = self.loop.add_timeout(self.cycle_time, self.on_timeout)

        try:
            if not self.connection:
                await self.connect_to_database()

            await self.store_message(message_box, message)
        except DatabaseWriteFailed:
            logger.exception('store failed. while connection')

            # 失敗したので後始末
            print('1')
            try:
                print('2')
                await self.cleanup_database()
                print('3')
            except:
                import traceback

                print('-=-=-=-=-=-=-=')
                traceback.print_exc()
                print('3')
            return False

        return True

    async def commit(self, flush_all=False):
        """commit.
        TODO: Fill blank

        :param bool flush_all:
        """
        await self.flush_timed_db(flush_all)

    # private in executor
    @run_on_executor
    def connect_to_database(self):
        """DBにつなぐ"""
        assert self.connection is None
        self.connection = self.database.connect()

    @run_on_executor
    def cleanup_database_sync(self, rollback):
        self.write_count = None

        if self.connection:
            self.connection.close()
            self.connection = None

    @run_on_executor
    def flush_timed_db(self, flush_all=False):
        """commit_transaction.
        TODO: Fill blank

        :param bool flush_all:
        """
        # commit TimeDB
        if flush_all:
            self.time_db_bundle.update(self.updates)
            self.updates = []
        elif self.updates:
            # lastのtimestamp秒以外を反映
            last_timestamp = math.floor(self.updates[-1][1])
            for idx, (box_id, timestamp) in enumerate(self.updates):
                if timestamp >= last_timestamp:
                    break
            if idx:
                updates, self.updates = self.updates[:idx], self.updates[idx:]
                self.time_db_bundle.update(updates)

        # remove timeout and reset
        if self.timeout:
            self.loop.remove_timeout(self.timeout)
            self.timeout = None
        self.write_count = None

    @run_on_executor
    def store_message(self, message_box, message):
        assert self.connection is not None

        if self.updates:
            if message.timestamp < self.updates[-1][1]:
                logger.error(
                    'bad timestamp, time is rolling back. message:%s queued_latest:%s', message.timestamp,
                    self.updates[-1][1]
                )

        self.database.store_message(message_box, message, connection=self.connection)
        self.updates.append((message.box_id, message.timestamp))
        self.write_count += 1

    # private
    async def cleanup_database(self, rollback=True):
        if self.timeout:
            self.loop.remove_timeout(self.timeout)
            self.timeout = None

        await self.cleanup_database_sync(rollback)

    async def on_timeout(self):
        """タイムアウト."""
        self.timeout = None
        await self.flush_timed_db()
