# -*- coding: utf-8 -*-

"""circle_coreのDBとの接続を取り仕切る"""

from __future__ import absolute_import

import datetime
import logging
import math
import threading
import time
import uuid

from base58 import b58encode
from click import get_current_context
from six import PY3
import sqlalchemy as sa
from sqlalchemy import sql
from sqlalchemy.dialects import mysql
from sqlalchemy.orm import sessionmaker
from sqlalchemy.schema import CreateColumn, SchemaVisitor
import sqlalchemy.sql.ddl
import tornado.ioloop

# project module
from circle_core.exceptions import MigrationError
from .constants import CRDataType
from .message import ModuleMessage, ModuleMessagePrimaryKey
from .models import Module, Schema
from .timed_db import TimedDBBundle

if PY3:
    from typing import List


META_TABLE_NAME = 'meta'
TABLE_OPTIONS = {
    'mysql_engine': 'InnoDB',
    'mysql_charset': 'utf8mb4',
}
logger = logging.getLogger(__name__)


class Database(object):
    """CircleCoreでのセンサデータ書き込み先DBを管理するクラス"""

    def __init__(self, database_url, time_db_dir):
        """
        @constructor

        :param str database_url: SQLAlchemy的DBのURL

        """
        self._engine = sa.create_engine(database_url)
        self._session = sessionmaker(bind=self._engine, autocommit=True)

        self._metadata = sa.MetaData()
        self._metadata.reflect(self._engine)

        self._time_db_dir = time_db_dir

        self._thread_id = None

    def connect(self):
        return self._engine.connect()
        # self._register_meta_table()

    # def _register_meta_table(self):
    #     self.table_meta = sa.Table(
    #         META_TABLE_NAME, self._metadata,
    #         sa.Column('key', mysql.VARCHAR(255, charset='ascii', collation='ascii_bin'), primary_key=True),
    #         sa.Column('value', sa.Text()),
    #         **TABLE_OPTIONS
    #     )

    # def register_message_boxes(self, boxes, schemas):
    #     """
    #     望むべきスキーマとモジュールを登録する

    #     :param List[MessageBox] boxes: メッセージボックスのリスト
    #     """
    #     for box in boxes:
    #         self.make_table_for_message_box(box)

    def make_table_for_message_box(self, message_box):
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

    # def diff_database(self):
    #     """
    #     DBをスキーマ、モジュールの設定に合わせて変更する必要があるかを調査する
    #     結果にエラーがあれば、MigrationError例外が起こる

    #     see: https://github.com/openstack/sqlalchemy-migrate/blob/master/migrate/versioning/schemadiff.py

    #     :return DiffResult: 検証結果
    #     """

    #     # 論理MetadataをVisitして、現実Databaseとの差異を確認
    #     logger.info('start checking database')
    #     diff_result = DiffResult()
    #     self._engine._run_visitor(
    #         DatabaseDiff,
    #         self._metadata,
    #         diff_result=diff_result,
    #     )

    #     return diff_result

    # def migrate(self):
    #     """
    #     DBをスキーマ、モジュールの設定に合わせて変更する
    #     結果にエラーがあれば、MigrationError例外が起こる
    #     """
    #     diff = self.diff_database()
    #     if diff.error_tables:
    #         raise MigrationError

    #     if diff.is_ok():
    #         logger.info('no need to migrate db')
    #         return

    #     logger.info('start migration')
    #     with self._engine.begin() as conn:
    #         for table in diff.new_tables:
    #             logger.info('  create new table %s', table.name)
    #             table.create(conn)

    #         for table in diff.alter_tables:
    #             logger.info('  drop and create table %s', table.name)
    #             table.drop(conn)
    #             table.create(conn)

    #     # poolの中のconnectionが古いTable情報をキャッシュしちゃってる？とかで怪しい挙動になるので、全部破棄する
    #     self._engine.dispose()

    def make_table_name_for_message_box(self, box_or_uuid):
        """

        :param MessageBox or UUID box:
        :return str:
        """
        if not isinstance(box_or_uuid, uuid.UUID):
            box_or_uuid = box_or_uuid.uuid

        return 'message_box_' + b58encode(box_or_uuid.bytes)

    def find_table_for_message_box(self, message_box, create_if_not_exsts=True):
        table_name = self.make_table_name_for_message_box(message_box)
        table = None
        if table_name in self._metadata.tables:
            # table already exists and registered to metadata
            table = self._metadata.tables[table_name]
        else:
            if create_if_not_exsts:
                # table not exists or not registered to metadata
                table = self.make_table_for_message_box(message_box)

        return table

    # def last_message_identifier_for_box(self, box):  # TODO: MessageBoxのメソッドにする
    #     session = self._session()
    #     with session.begin():
    #         table = self.find_table_for_message_box(box)
    #         identifier = session.query(table) \
    #             .with_entities(table.columns._created_at, table.columns._counter) \
    #             .order_by(table.columns._created_at.desc(), table.columns._counter.desc()) \
    #             .first()

    #         if identifier is None:
    #             return 0, 0
    #         else:
    #             created_at, counter = identifier

    #     return float(created_at), counter

    def store_message(self, message_box, message, connection=None):
        """databaseにmessageを保存する"""
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
        assert connection, 'TODO: create new connection if not present it'
        assert self._thread_id == threading.get_ident()
        self._check_thread()

        table = self.find_table_for_message_box(message_box, create_if_not_exsts=False)
        if table is not None:
            table.drop(self._engine)
            self._metadata.remove(table)

    def _check_thread(self):
        if self._thread_id is None:
            self._thread_id = threading.get_ident()
        assert self._thread_id == threading.get_ident()

    def get_latest_primary_key(self, message_box, connection=None):
        if not connection:
            connection = self._engine.connect()

        table = self.find_table_for_message_box(message_box)
        query = (
            sql.select([table.c._created_at, table.c._counter])
            .order_by(table.c._created_at.desc(), table.c._counter.desc())
            .limit(1)
        )
        rows = connection.execute(query).fetchall()
        if not rows:
            return None
        return ModuleMessagePrimaryKey(ModuleMessage.make_timestamp(rows[0][0]), rows[0][1])

    def enum_message_from(self, message_box, head=None, connection=None):
        assert connection, 'TODO: create new connection if not present it'
        assert head is None or isinstance(head, ModuleMessagePrimaryKey)

        table = self.find_table_for_message_box(message_box, create_if_not_exsts=False)
        if table is None:
            return

        query = sql.select([table]).order_by(table.c._created_at.asc(), table.c._counter.asc())
        if head:
            query = query.where(table.c._created_at >= head.timestamp)

        for row in connection.execute(query):
            row = dict(row)
            message = ModuleMessage(message_box.uuid, row.pop('_created_at'), row.pop('_counter'), row)

            if head:
                if message.timestamp < head.timestamp or \
                   (message.timestamp == head.timestamp and message.counter <= head.counter):
                    # logger.info('skip message %s', message)
                    continue

            yield message

# class DiffResult(object):
#     """
#     DB比較結果

#     :param List[sa.Table] new_tables: 新規に作る必要のあるTable
#     :param List[sa.Table] alter_tables: AlterするTable
#     :param List[sa.Table] error_tables: エラーがあって変更できないTable
#     """
#     def __init__(self):
#         self.new_tables = []
#         self.alter_tables = []
#         self.error_tables = []

#     def is_ok(self):
#         return all([not self.new_tables, not self.alter_tables, not self.error_tables])


# class DatabaseDiff(SchemaVisitor):
#     """
#     スキーマのDBと、現実のDBの比較をして結果を返す

#     :param Any dialect: dialect
#     :param Any connection: connection
#     :param DiffResult diff_result: 結果格納用のTable
#     :param sa.MetaData db_metadata: 結果格納用のTable
#     """
#     __visit_name__ = 'database_diff'

#     def __init__(self, dialect, connection, diff_result, *args, **kwargs):
#         """
#         constructor

#         :param Any dialect: dialect
#         :param Any connection: connection
#         :param DiffResult diff_result: 結果格納用のTable
#         """
#         super(DatabaseDiff, self).__init__()
#         self.dialect = dialect
#         self.connection = connection
#         self.diff_result = diff_result
#         self.db_metadata = sa.MetaData()
#         # self.db_metadata = db_metadata

#     def visit_metadata(self, metadata):  # NOQA
#         tables = sqlalchemy.sql.ddl.sort_tables(metadata.tables.values())
#         for table in tables:
#             if table is not None:
#                 self.traverse_single(table)

#     def visit_table(self, table):
#         extend_existing = False,
#         autoload_replace = True

#         # tableがあるかチェック
#         self.dialect.validate_identifier(table.name)
#         effective_schema = self.connection.schema_for_object(table)
#         if effective_schema:
#             self.dialect.validate_identifier(effective_schema)
#         has_table = self.dialect.has_table(
#             self.connection, table.name, schema=effective_schema)

#         # errors = []
#         logger.info('  checking `%s`...', table.name)

#         if not has_table:
#             # tableが無いので作成する
#             logger.info('    no table found at dest database')
#             self.diff_result.new_tables.append(table)
#         else:
#             # tableがあるのでdiffをとる
#             db_table = sa.Table(table.name, self.db_metadata, **{
#                 'autoload': True,
#                 'autoload_with': self.connection,
#                 'extend_existing': extend_existing,
#                 'autoload_replace': autoload_replace
#             })

#             # tableのカラムをすべてなめて、diffがあるか調べる
#             # 現在のところdb_tableにあって、tableにないカラムは無視している
#             diff = False
#             for col_me in table.get_children():
#                 if col_me.key not in db_table.c:
#                     logger.info('    col `%s` ... not found', col_me.key)
#                     diff = True
#                 else:
#                     col_db = db_table.c[col_me.key]
#                     if isinstance(col_db.type, sa.DECIMAL):
#                         col_db.type = sa.NUMERIC(col_db.type.precision, col_db.type.scale)

#                     # 本当はdialectつけて比較すべきだと思うのだけど、autoloadでそこまで読み込まないらしく、必ず差が出てしまう
#                     # col_me_str = str(CreateColumn(col_me).compile(dialect=self.dialect))
#                     # col_db_str = str(CreateColumn(col_db).compile(dialect=self.dialect))
#                     col_me_str = str(CreateColumn(col_me).compile())
#                     col_db_str = str(CreateColumn(col_db).compile())

#                     if col_me_str != col_db_str:
#                         logger.info('    col `%s` ... different %r <> %r', col_me.key, col_me_str, col_db_str)
#                         diff = True
#                     else:
#                         logger.info('    col `%s` ok', col_me.key)

#             if diff:
#                 # db_tableの要素数を数える
#                 count = self.connection.scalar(db_table.count())
#                 if count > 0:
#                     # 空っぽじゃないので、とりあえずエラーにしている
#                     logger.info('    table is not empty')
#                     self.diff_result.error_tables.append(table)
#                 else:
#                     # 空っぽであればdrop->createで作り直せる
#                     logger.info('    table is empty')
#                     self.diff_result.alter_tables.append(table)
    def make_writer(self, cycle_time=10.0, cycle_count=100):
        return QueuedWriter(self, self._time_db_dir, cycle_time, cycle_count)


def make_sqlcolumn_from_datatype(name, datatype):
    """schemaの型に応じて、SQLAlchemyのColumnを返す

    :param str name: カラム名
    :param CRDataType datatype: データ型
    :return sa.Column: カラム
    """

    assert not name.startswith('_')
    datatype = CRDataType.from_text(datatype)

    if datatype == CRDataType.INT:
        coltype = sa.Integer()
    elif datatype == CRDataType.FLOAT:
        coltype = sa.Float()
    elif datatype == CRDataType.TEXT:
        coltype = sa.Text()
    else:
        assert 0, 'not implemented yet'

    return sa.Column(name, coltype)


class QueuedWriter(object):
    def __init__(self, database, time_db_dir, cycle_time=10.0, cycle_count=100):
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
        if not self.transaction:
            return
        self.commit_transaction(flush_all)

    def begin_transaction(self):
        assert self.transaction is None
        assert self.timeout is None
        self.transaction, self.write_count, self.transaction_begin = self.connection.begin(), 0, time.time()
        self.timeout = tornado.ioloop.IOLoop.current().add_timeout(self.cycle_time, self.on_timeout)

    def commit_transaction(self, flush_all=False):
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
        self.timeout = None
        self.commit_transaction()
