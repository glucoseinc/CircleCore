# -*- coding: utf-8 -*-

"""circle_coreのDBとの接続を取り仕切る."""

from __future__ import absolute_import

# system module
import datetime
import logging
import math
import threading
import time
import uuid

# community module
from base58 import b58encode
from six import PY3
import sqlalchemy as sa
from sqlalchemy.engine import Connection, Engine, Transaction
from sqlalchemy.orm import sessionmaker
import tornado.ioloop
from tornado.ioloop import _Timeout

# project module
from .constants import CRDataType
from .message import ModuleMessage, ModuleMessagePrimaryKey
from .models import MessageBox
from .timed_db import TimedDBBundle

if PY3:
    from typing import Generator, List, Optional, Union


TABLE_OPTIONS = {
    'mysql_engine': 'InnoDB',
    'mysql_charset': 'utf8mb4',
}
logger = logging.getLogger(__name__)


class Database(object):
    """CircleCoreでのセンサデータ書き込み先DBを管理するクラス.

    :param Engine _engine: SQLAlchemy Engine
    :param sessionmaker _session: SQLAlchemy sessionmaker
    :param sa.MetaData _metadata: SQLAlchemy MetaData
    :param str _time_db_dir: 時系列DBのPath
    :param Optional[int] _thread_id: Thread ID
    """

    def __init__(self, database_url, time_db_dir):
        """init.

        :param str database_url: DBのURL(RFC-1738準拠)
        :param str time_db_dir: 時系列DBのPath
        """
        self._engine = sa.create_engine(database_url)
        self._session = sessionmaker(bind=self._engine, autocommit=True)

        self._metadata = sa.MetaData()
        self._metadata.reflect(self._engine)

        self._time_db_dir = time_db_dir

        self._thread_id = None

    def connect(self):
        """Return a new Connection object.

        :return: Connection
        :rtype: Connection
        """
        return self._engine.connect()

    def make_table_for_message_box(self, message_box):
        """MessageBox Tableを生成する.

        :param MessageBox message_box: MessageBox
        :return: MessageBox Table
        :rtype: sa.Table
        """
        # define table
        table_name = self.make_table_name_for_message_box(message_box)

        # define columns
        columns = [
            # FIXME: 常にMessageからtimestampを注入するのでDEFALUT CURRENT_TIMESTAMPを切りたいが方法が分からない
            sa.Column('_created_at', sa.Numeric(16, 6, asdecimal=True), nullable=False),
            sa.Column('_counter', sa.Integer(), nullable=False, default=0),
        ]
        for prop in message_box.schema.properties:
            columns.append(make_sqlcolumn_from_datatype(prop.name, prop.type))
        columns.append(
            sa.PrimaryKeyConstraint('_created_at', '_counter')
        )
        kwargs = TABLE_OPTIONS.copy()
        # kwargs['autoload_with'] = self._engine
        table = sa.Table(table_name, self._metadata, *columns, **kwargs)

        # make table
        table.create(self._engine, checkfirst=True)

        return table

    def make_table_name_for_message_box(self, box_or_uuid):
        """MessageBox Table名を生成する.

        :param Union[MessageBox, uuid.UUID] box_or_uuid:
        :return str:
        """
        if not isinstance(box_or_uuid, uuid.UUID):
            box_or_uuid = box_or_uuid.uuid

        return 'message_box_' + b58encode(box_or_uuid.bytes)

    def find_table_for_message_box(self, message_box, create_if_not_exists=True):
        """MessageBox Tableを取得する.

        :param MessageBox message_box: 取得するMessageBox
        :param bool create_if_not_exists: Tableが存在しなければ作成する
        :return: MessageBox Table
        :rtype: Optional[sa.Table]
        """
        table_name = self.make_table_name_for_message_box(message_box)
        table = None
        if table_name in self._metadata.tables:
            # table already exists and registered to metadata
            table = self._metadata.tables[table_name]
        else:
            if create_if_not_exists:
                # table not exists or not registered to metadata
                table = self.make_table_for_message_box(message_box)

        return table

    def store_message(self, message_box, message, connection=None):
        """Databaseにmessageを保存する.

        :param MessageBox message_box: MessageBox
        :param ModuleMessage message: message
        :param Optional[Connection] connection: Connection
        """
        assert connection, 'TODO: create new connection if not present it'
        self._check_thread()

        table = self.find_table_for_message_box(message_box)
        query = table.insert().values(
            _created_at=message.timestamp,
            _counter=message.counter,
            **message.payload
        )
        connection.execute(query)

    def drop_message_box(self, message_box, connection=None):
        """MessageBox Tableを削除する.

        :param MessageBox message_box: MessageBox
        :param Optional[Connection] connection: Connection
        """
        if not connection:
            connection = self._engine.connect()

        table = self.find_table_for_message_box(message_box, create_if_not_exists=False)
        if table is not None:
            table.drop(self._engine)
            self._metadata.remove(table)

    def _check_thread(self):
        """Threadの整合性をチェックする."""
        if self._thread_id is None:
            self._thread_id = threading.get_ident()
        assert self._thread_id == threading.get_ident()

    def get_latest_primary_key(self, message_box, connection=None):
        """get latest primary key.
        TODO: fill blank

        :param MessageBox message_box: MessageBox
        :param Optional[Connection] connection: Connection
        :return:
        :rtype:
        """
        if not connection:
            connection = self._engine.connect()

        table = self.find_table_for_message_box(message_box)
        query = (
            sa.sql.select([table.c._created_at, table.c._counter])
            .order_by(table.c._created_at.desc(), table.c._counter.desc())
            .limit(1)
        )
        rows = connection.execute(query).fetchall()
        if not rows:
            return None
        return ModuleMessagePrimaryKey(ModuleMessage.make_timestamp(rows[0][0]), rows[0][1])

    def count_messages(self, message_box, head=None, limit=None, connection=None):
        """メッセージ数を返す.

        :param MessageBox message_box: MessageBox
        :param Optional[ModuleMessagePrimaryKey] head: HEAD
        :param Optional[int] limit: 取得数の上限
        :param Optional[Connection] connection: Connection
        :return: メッセージ数
        :rtype: int
        """
        if not connection:
            connection = self._engine.connect()

        table = self.find_table_for_message_box(message_box, create_if_not_exists=False)
        if table is None:
            return 0

        return connection.scalar(sa.sql.select([sa.func.count()]).select_from(table))

    def enum_messages(self, message_box, start=None, end=None, head=None, limit=None, order='asc', connection=None):
        """head以降のメッセージを返す.

        :param MessageBox message_box: MessageBox
        :param Optional[float] start: 開始日
        :param Optional[float] end: 終了日
        :param Optional[ModuleMessagePrimaryKey] head: HEAD
        :param Optional[int] limit: 取得数の上限
        :param str order: asc -> 古い順, desc -> 新しい順
        :param Optional[Connection] connection: Connection
        :return: メッセージジェネレータ
        :rtype: Generator[ModuleMessage, ModuleMessage, ModuleMessage]
        """
        assert order in ('desc', 'asc')
        if not connection:
            connection = self._engine.connect()

        assert head is None or isinstance(head, ModuleMessagePrimaryKey)

        table = self.find_table_for_message_box(message_box, create_if_not_exists=False)
        if table is None:
            return

        query = sa.sql.select([table])

        if order == 'asc':
            query = query.order_by(table.c._created_at.asc(), table.c._counter.asc())
        else:
            query = query.order_by(table.c._created_at.desc(), table.c._counter.desc())

        if start:
            query = query.where(table.c._created_at >= start)
        if end:
            query = query.where(table.c._created_at <= end)
        if head:
            query = query.where(table.c._created_at >= head.timestamp)
        if limit:
            query = query.limit(limit)

        for row in connection.execute(query):
            row = dict(row)
            message = ModuleMessage(message_box.uuid, row.pop('_created_at'), row.pop('_counter'), row)

            if head:
                if message.timestamp < head.timestamp or \
                   (message.timestamp == head.timestamp and message.counter <= head.counter):
                    # logger.info('skip message %s', message)
                    continue

            yield message

    def make_writer(self, cycle_time=10.0, cycle_count=100):
        """make_writer.
        TODO: fill blank

        :param float cycle_time:
        :param int cycle_count:
        :return:
        :rtype: QueuedWriter
        """
        return QueuedWriter(self, self._time_db_dir, cycle_time, cycle_count)


def make_sqlcolumn_from_datatype(name, datatype):
    """schemaの型に応じて、SQLAlchemyのColumnを返す.

    :param str name: カラム名
    :param CRDataType datatype: データ型
    :return sa.Column: カラム
    """

    assert not name.startswith('_')

    coltypes = {
        CRDataType.INT: sa.INTEGER,
        CRDataType.FLOAT: sa.FLOAT,
        CRDataType.BOOL: sa.BOOLEAN,
        CRDataType.STRING: sa.TEXT,
        CRDataType.BYTES: sa.BLOB,
        CRDataType.DATE: sa.DATE,
        CRDataType.DATETIME: sa.DATETIME,
        CRDataType.TIME: sa.TIME,
        CRDataType.TIMESTAMP: sa.TIMESTAMP,
    }
    coltype = coltypes[CRDataType(datatype.upper())]()

    return sa.Column(name, coltype)


class QueuedWriter(object):
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

    def store(self, message_box, message):
        """store.
        TODO: Fill blank

        :param MessageBox message_box:
        :param ModuleMessage message:
        """
        if not isinstance(message, ModuleMessage):
            raise ValueError

        if not self.transaction:
            self.begin_transaction()

        self.database.store_message(message_box, message, connection=self.connection)
        self.updates.append((message.box_id, message.timestamp))
        self.write_count += 1

        if self.write_count >= self.cycle_count:
            self.commit_transaction()

    def commit(self, flush_all=False):
        """commit.
        TODO: Fill blank

        :param bool flush_all:
        """
        if not self.transaction:
            return
        self.commit_transaction(flush_all)

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
                updates, self.updates = self.updates[:idx - 1], self.updates[idx - 1:]
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
