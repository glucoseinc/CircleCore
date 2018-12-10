import datetime
import time
from typing import TYPE_CHECKING

import tornado.ioloop

from .base import DBWriter
from ..logger import logger
from ..message import ModuleMessage
from ..timed_db import TimedDBBundle

if TYPE_CHECKING:
    from tornado.ioloop import _Timeout


class QueuedWriter(DBWriter):
    """QueuedWriter.
    TODO: Fill blank

    :param Database database:
    :param TimedDBBundle time_db_bundle:
    :param List updates:
    :param float cycle_count:
    :param int cycle_time:
    :param Connection connection:
    :param Optional[Transaction] transaction:
    :param Optional[_Timeout] timeout:
    """

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

        # RDB
        self.database = database
        # 時系列DB
        self.time_db_bundle = TimedDBBundle(time_db_dir)
        # timed dbのアップデート用にlist((box_id, timestamp))を記録する
        self.updates = []

        self.cycle_count = cycle_count
        self.cycle_time = datetime.timedelta(seconds=cycle_time)

        self.connection = self.database.connect()
        self.transaction = None
        self.timeout = None

    # override
    async def store(self, message_box, message) -> bool:
        """store.
        TODO: Fill blank

        :param MessageBox message_box:
        :param ModuleMessage message:
        """
        if not isinstance(message, ModuleMessage):
            raise ValueError

        if not self.transaction:
            self.begin_transaction()

        if self.updates:
            if message.timestamp < self.updates[-1][1]:
                logger.error(
                    'bad timestamp, time is rolling back. message:%s queued_latest:%s', message.timestamp,
                    self.updates[-1][1]
                )

        self.database.store_message(message_box, message, connection=self.connection)
        self.updates.append((message.box_id, message.timestamp))
        self.write_count += 1

        if self.write_count >= self.cycle_count:
            self.commit_transaction()

        return True

    async def commit(self, flush_all=False):
        """commit.
        TODO: Fill blank

        :param bool flush_all:
        """
        if not self.transaction:
            return
        self.commit_transaction(flush_all)

    # private
    def begin_transaction(self):
        """Transactionを開始する."""
        assert self.transaction is None
        assert self.timeout is None
        self.transaction, self.write_count, self.transaction_begin = self.connection.begin(), 0, time.time()
        self.timeout = tornado.ioloop.IOLoop.current().add_timeout(self.cycle_time, self.on_timeout)

    def commit_transaction(self, flush_all=False):
        """commit_transaction.
        TODO: Fill blank

        :param bool flush_all:
        """
        # commit RDB
        logger.debug('commit, data count=%d, interval=%f', self.write_count, time.time() - self.transaction_begin)
        self.transaction.commit()

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
            tornado.ioloop.IOLoop.current().remove_timeout(self.timeout)
            self.timeout = None
        self.transaction = self.write_count = self.transaction_begin = None

    def on_timeout(self):
        """タイムアウト."""
        self.timeout = None
        self.commit_transaction()
