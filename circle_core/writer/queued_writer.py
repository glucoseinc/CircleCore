import datetime
import math
import threading
from concurrent.futures import ThreadPoolExecutor
from typing import List, Tuple, Optional, TYPE_CHECKING

import sqlalchemy.exc

import tornado.ioloop
from tornado.concurrent import run_on_executor

from typing_extensions import Protocol

from .base import DBWriter
from ..exceptions import DatabaseWriteFailed
from ..logger import logger
from ..message import ModuleMessage
from ..timed_db import TimedDBBundle

if TYPE_CHECKING:
    from tornado.ioloop import _Timeout
    import uuid

    from ..models import MessageBox
    from ..types import Timestamp

# 接続不良時の再接続への間隔
RETRY_TIMEOUT = datetime.timedelta(seconds=2)


class QueuedDBWriterDelegate(Protocol):

    async def on_reconnect(self) -> None:
        """再接続できた"""


class QueuedDBWriter(DBWriter):
    """QueuedWriter.
    TODO: Fill blank

    :param Database database:
    :param TimedDBBundle time_db_bundle:
    :param List updates:  TimeDBに書き込むためのデータを持っている
    :param float cycle_count:
    :param int cycle_time:
    :param Connection connection:
    """
    delegate: Optional[QueuedDBWriterDelegate]
    retry_connect_timeout: 'Optional[_Timeout]'
    timeout: 'Optional[_Timeout]'
    tls_connection: threading.local
    updates: 'List[Tuple[uuid.UUID, Timestamp]]'
    write_count: int

    # database周りのexecution, 常に直列でやる
    executor = ThreadPoolExecutor(1, thread_name_prefix='queued_writer_thread_')

    def __init__(
        self,
        database,
        time_db_dir,
        *,
        cycle_time=10.0,
        cycle_count=100,
        delegate: Optional[QueuedDBWriterDelegate] = None
    ):
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

        self.tls_connection = threading.local()
        self.timeout = None

        # 接続再試行
        self.retry_connect_timeout = None

        self.delegate = delegate
        self.write_count = 0

    # override
    async def store(self, message_box: 'MessageBox', message: ModuleMessage) -> bool:
        """store.
        TODO: Fill blank

        storeはシリアライズされているんだっけ???
        """
        if not self.timeout:
            self.timeout = self.loop.add_timeout(self.cycle_time, self.on_timeout)
        try:
            # if not self.connection:
            #     await self.connect_to_database()
            await self.store_message(message_box, message)
        except DatabaseWriteFailed:
            # logger.exception('store failed. while connection')
            logger.error('store failed. while connection')

            # 失敗したので
            if not self.retry_connect_timeout:
                self.retry_connect_timeout = self.loop.add_timeout(RETRY_TIMEOUT, self.reconncet)

            # 失敗したので後始末
            await self.cleanup_database()

            return False
        except:  # noqa
            logger.exception('Uncatched exception')
            raise

        return True

    async def flush(self, flush_all=False):
        """commit.
        TODO: Fill blank

        :param bool flush_all:
        """
        await self.flush_timed_db(flush_all)

    # private in executor
    @run_on_executor
    def connect_to_database(self):
        """DBにつなぐ"""
        connection = getattr(self.tls_connection, 'connection', None)
        if connection:
            connection.close()
        connection = self.database.connect()
        self.tls_connection.connection = connection

    @run_on_executor
    def cleanup_database_sync(self):
        if self.timeout:
            self.loop.remove_timeout(self.timeout)
            self.timeout = None

        connection = getattr(self.tls_connection, 'connection', None)
        if connection:
            try:
                connection.close()
            except sqlalchemy.exc.DatabaseError:
                pass
        self.tls_connection = threading.local()

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
        self.write_count = 0

    @run_on_executor
    def store_message(self, message_box, message):
        connection = getattr(self.tls_connection, 'connection', None)
        if not connection:
            try:
                connection = self.database.connect()
            except sqlalchemy.exc.DatabaseError as exc:
                logger.error('Failed to connect database')
                raise DatabaseWriteFailed(exc)
            except Exception as exc:  # noqa
                logger.error('Uncatched exception, whie connecting to database')
                raise DatabaseWriteFailed(exc)
            self.tls_connection.connection = connection

        if self.updates:
            if message.timestamp < self.updates[-1][1]:
                logger.error(
                    'bad timestamp, time is rolling back. message:%s queued_latest:%s', message.timestamp,
                    self.updates[-1][1]
                )

        self.database.store_message(message_box, message, connection=connection)
        self.updates.append((message.box_id, message.timestamp))
        self.write_count += 1

    # private
    async def cleanup_database(self):
        if self.timeout:
            self.loop.remove_timeout(self.timeout)
            self.timeout = None

        await self.cleanup_database_sync()

    async def on_timeout(self):
        """タイムアウト."""
        self.timeout = None
        await self.flush_timed_db()

    async def reconncet(self):
        self.retry_connect_timeout = None

        try:
            await self.connect_to_database()
        except (DatabaseWriteFailed, sqlalchemy.exc.DatabaseError):
            logger.info('Reconnect failed, retry after %r secs', RETRY_TIMEOUT)
            self.retry_connect_timeout = self.loop.add_timeout(RETRY_TIMEOUT, self.reconncet)
            return
        except:  # noqa
            logger.exception('Uncatched error while reconnect')
        else:
            logger.info('Database reconnected')
            if self.delegate:
                await self.delegate.on_reconnect()
