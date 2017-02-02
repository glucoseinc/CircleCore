# -*- coding: utf-8 -*-

"""circle_coreのDBとの接続を取り仕切る"""

from __future__ import absolute_import

from time import mktime
import uuid

from base58 import b58encode
from click import get_current_context
from six import PY3
import sqlalchemy as sa
from sqlalchemy.dialects import mysql
from sqlalchemy.orm import sessionmaker
from sqlalchemy.schema import CreateColumn, SchemaVisitor
import sqlalchemy.sql.ddl

# project module
from circle_core.exceptions import MigrationError
from circle_core.helpers.metadata import metadata
from circle_core.logger import get_stream_logger
from .constants import CRDataType
from .models.module import Module
from .models.schema import Schema

if PY3:
    from typing import List


META_TABLE_NAME = 'meta'
TABLE_OPTIONS = {
    'mysql_engine': 'InnoDB',
    'mysql_charset': 'utf8mb4',
}
# TODO temporary
logger = get_stream_logger('crcr.database')


class Database(object):
    """CircleCoreでのセンサデータ書き込み先DBを管理するクラス"""

    def __init__(self, database_url):
        """
        @constructor

        :param str database_url: SQLAlchemy的DBのURL

        """
        self._engine = sa.create_engine(database_url)
        self._session = sessionmaker(bind=self._engine, autocommit=True)

        self._metadata = sa.MetaData()
        self._register_meta_table()

    def _register_meta_table(self):
        self.table_meta = sa.Table(
            META_TABLE_NAME, self._metadata,
            sa.Column('key', mysql.VARCHAR(255, charset='ascii', collation='ascii_bin'), primary_key=True),
            sa.Column('value', sa.Text()),
            **TABLE_OPTIONS
        )

    def register_message_boxes(self, boxes, schemas):
        """
        望むべきスキーマとモジュールを登録する

        :param List[MessageBox] boxes: メッセージボックスのリスト
        """
        for box in boxes:
            table_name = self.make_table_name_for_message_box(box)

            # define columns
            columns = [
                # FIXME: 常にMessageからtimestampを注入するのでDEFALUT CURRENT_TIMESTAMPを切りたいが方法が分からない
                sa.Column('_created_at', sa.Numeric(16, 6, asdecimal=True), nullable=False),
                sa.Column('_counter', sa.Integer(), nullable=False, default=0),
            ]
            for prop in box.schema.properties:
                columns.append(make_sqlcolumn_from_datatype(prop.name, prop.type))
            columns.append(
                sa.PrimaryKeyConstraint('_created_at', '_counter')
            )
            sa.Table(table_name, self._metadata, *columns, **TABLE_OPTIONS)

    def diff_database(self):
        """
        DBをスキーマ、モジュールの設定に合わせて変更する必要があるかを調査する
        結果にエラーがあれば、MigrationError例外が起こる

        see: https://github.com/openstack/sqlalchemy-migrate/blob/master/migrate/versioning/schemadiff.py

        :return DiffResult: 検証結果
        """

        # 論理MetadataをVisitして、現実Databaseとの差異を確認
        logger.info('start checking database')
        diff_result = DiffResult()
        self._engine._run_visitor(
            DatabaseDiff,
            self._metadata,
            diff_result=diff_result,
        )

        return diff_result

    def migrate(self):
        """
        DBをスキーマ、モジュールの設定に合わせて変更する
        結果にエラーがあれば、MigrationError例外が起こる
        """
        diff = self.diff_database()
        if diff.error_tables:
            raise MigrationError

        if diff.is_ok():
            logger.info('no need to migrate db')
            return

        logger.info('start migration')
        with self._engine.begin() as conn:
            for table in diff.new_tables:
                logger.info('  create new table %s', table.name)
                table.create(conn)

            for table in diff.alter_tables:
                logger.info('  drop and create table %s', table.name)
                table.drop(conn)
                table.create(conn)

        # poolの中のconnectionが古いTable情報をキャッシュしちゃってる？とかで怪しい挙動になるので、全部破棄する
        self._engine.dispose()

    def make_table_name_for_message_box(self, box_or_uuid):
        """

        :param MessageBox or UUID box:
        :return str:
        """
        if not isinstance(box_or_uuid, uuid.UUID):
            box_or_uuid = box_or_uuid.uuid

        assert(isinstance(box_or_uuid, uuid.UUID), '{!r} is not a UUID'.format(box_or_uuid))
        return 'message_box_' + b58encode(box_or_uuid.bytes)

    def find_table_for_message_box(self, box):  # これらも各modelのメソッドにした方がいいかなあ
        return sa.Table(
            self.make_table_name_for_message_box(box),
            self._metadata,
            autoload=True,
            autoload_with=self._engine
        )

    def last_message_identifier_for_box(self, box):  # TODO: MessageBoxのメソッドにする
        session = self._session()
        with session.begin():
            table = self.find_table_for_message_box(box)
            identifier = session.query(table) \
                .with_entities(table.columns._created_at, table.columns._counter) \
                .order_by(table.columns._created_at.desc(), table.columns._counter.desc()) \
                .first()

            if identifier is None:
                return 0, 0
            else:
                created_at, counter = identifier

        return float(created_at), counter


class DiffResult(object):
    """
    DB比較結果

    :param List[sa.Table] new_tables: 新規に作る必要のあるTable
    :param List[sa.Table] alter_tables: AlterするTable
    :param List[sa.Table] error_tables: エラーがあって変更できないTable
    """
    def __init__(self):
        self.new_tables = []
        self.alter_tables = []
        self.error_tables = []

    def is_ok(self):
        return all([not self.new_tables, not self.alter_tables, not self.error_tables])


class DatabaseDiff(SchemaVisitor):
    """
    スキーマのDBと、現実のDBの比較をして結果を返す

    :param Any dialect: dialect
    :param Any connection: connection
    :param DiffResult diff_result: 結果格納用のTable
    :param sa.MetaData db_metadata: 結果格納用のTable
    """
    __visit_name__ = 'database_diff'

    def __init__(self, dialect, connection, diff_result, *args, **kwargs):
        """
        constructor

        :param Any dialect: dialect
        :param Any connection: connection
        :param DiffResult diff_result: 結果格納用のTable
        """
        super(DatabaseDiff, self).__init__()
        self.dialect = dialect
        self.connection = connection
        self.diff_result = diff_result
        self.db_metadata = sa.MetaData()
        # self.db_metadata = db_metadata

    def visit_metadata(self, metadata):  # NOQA
        tables = sqlalchemy.sql.ddl.sort_tables(metadata.tables.values())
        for table in tables:
            if table is not None:
                self.traverse_single(table)

    def visit_table(self, table):
        extend_existing = False,
        autoload_replace = True

        # tableがあるかチェック
        self.dialect.validate_identifier(table.name)
        effective_schema = self.connection.schema_for_object(table)
        if effective_schema:
            self.dialect.validate_identifier(effective_schema)
        has_table = self.dialect.has_table(
            self.connection, table.name, schema=effective_schema)

        # errors = []
        logger.info('  checking `%s`...', table.name)

        if not has_table:
            # tableが無いので作成する
            logger.info('    no table found at dest database')
            self.diff_result.new_tables.append(table)
        else:
            # tableがあるのでdiffをとる
            db_table = sa.Table(table.name, self.db_metadata, **{
                'autoload': True,
                'autoload_with': self.connection,
                'extend_existing': extend_existing,
                'autoload_replace': autoload_replace
            })

            # tableのカラムをすべてなめて、diffがあるか調べる
            # 現在のところdb_tableにあって、tableにないカラムは無視している
            diff = False
            for col_me in table.get_children():
                if col_me.key not in db_table.c:
                    logger.info('    col `%s` ... not found', col_me.key)
                    diff = True
                else:
                    col_db = db_table.c[col_me.key]
                    if isinstance(col_db.type, sa.DECIMAL):
                        col_db.type = sa.NUMERIC(col_db.type.precision, col_db.type.scale)

                    # 本当はdialectつけて比較すべきだと思うのだけど、autoloadでそこまで読み込まないらしく、必ず差が出てしまう
                    # col_me_str = str(CreateColumn(col_me).compile(dialect=self.dialect))
                    # col_db_str = str(CreateColumn(col_db).compile(dialect=self.dialect))
                    col_me_str = str(CreateColumn(col_me).compile())
                    col_db_str = str(CreateColumn(col_db).compile())

                    if col_me_str != col_db_str:
                        logger.info('    col `%s` ... different %r <> %r', col_me.key, col_me_str, col_db_str)
                        diff = True
                    else:
                        logger.info('    col `%s` ok', col_me.key)

            if diff:
                # db_tableの要素数を数える
                count = self.connection.scalar(db_table.count())
                if count > 0:
                    # 空っぽじゃないので、とりあえずエラーにしている
                    logger.info('    table is not empty')
                    self.diff_result.error_tables.append(table)
                else:
                    # 空っぽであればdrop->createで作り直せる
                    logger.info('    table is empty')
                    self.diff_result.alter_tables.append(table)


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
