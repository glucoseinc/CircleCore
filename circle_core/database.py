# -*- coding: utf-8 -*-
"""circle_coreのDBとの接続を取り仕切る."""

from __future__ import absolute_import

# system module
import datetime
import re
import threading
import uuid
from typing import Any, Dict, Mapping, Optional, TYPE_CHECKING

# community module
from base58 import b58encode

import sqlalchemy as sa
import sqlalchemy.exc
from sqlalchemy.orm import sessionmaker

# project module
from .constants import CRDataType
from .exceptions import BadDBQuery, DatabaseConnectionLost, DatabaseWriteFailed
from .logger import logger
from .message import ModuleMessage, ModuleMessagePrimaryKey
from .models import MessageBox
from .serialize import serialize
from .types import Path
from .utils import prepare_date

if TYPE_CHECKING:
    from .workers.blobstore import StoredBlob

TABLE_OPTIONS = {
    'mysql_engine': 'InnoDB',
    'mysql_charset': 'utf8mb4',
}
DATE_REX = re.compile(r'(\d{4})-(\d{1,2})-(\d{1,2})')


class Database(object):
    """CircleCoreでのセンサデータ書き込み先DBを管理するクラス.

    Args:
            database_url (str): DBのURL(RFC-1738準拠)
            time_db_dir (str): 時系列DBのPath

    Attributes:
        _engine (Engine): SQLAlchemy Engine
        _session (sessionmaker): SQLAlchemy sessionmaker
        _metadata (sa.MetaData): SQLAlchemy MetaData
        _time_db_dir (str): 時系列DBのPath
        _thread_id (Optional[int]): Thread ID
    """

    def __init__(
        self, database_url: str, time_db_dir: Path, log_dir: Path, *, connect_args: Optional[Mapping[str, Any]] = None
    ):
        """init.
        """
        if not log_dir:
            raise ValueError('log_dir required')
        self._engine = sa.create_engine(database_url, connect_args=connect_args or {})
        self._session = sessionmaker(bind=self._engine, autocommit=True)

        self._metadata = sa.MetaData()
        self._metadata.reflect(self._engine)
        self._time_db_dir = time_db_dir
        self._thread_id = None
        self._log_dir = log_dir

        # 現在把握している最新のメッセージキーを保存する(つまり、未コミットのものも含む)
        self._message_heads = self._get_current_message_heads()

    # public
    def store_message(self, message_box: 'MessageBox', message: 'ModuleMessage', *, connection=None) -> None:
        """Databaseにmessageを保存する.

        Args:
            message_box (circle_core.models.MessageBox): MessageBox
            message (ModuleMessage): message
            connection (Optional[Connection]): Connection
        """
        assert connection, 'TODO: create new connection if not present it'
        self._check_thread()

        previous_head = self._message_heads.get(message_box.uuid)
        if previous_head and previous_head >= message.primary_key:
            raise ValueError('message is older than latest head')

        table = self.find_table_for_message_box(message_box)

        try:
            query = table.insert().values(
                _created_at=message.timestamp, _counter=message.counter, **self.convert_payload(message_box, message)
            )
        except ValueError as exc:
            logger.exception('Bad message %r', exc)
            raise BadDBQuery

        try:
            connection.execute(query)
        except sqlalchemy.exc.DatabaseError as exc:
            # 接続エラーとかの場合 OperationalErrorがくる
            logger.exception('Failed to write message, %r', exc)

            if isinstance(exc, sqlalchemy.exc.InternalError):
                import pymysql.err

                if isinstance(exc.orig, pymysql.err.InternalError) and exc.orig.args[0] == 1292:
                    # pymysql.err.InternalError: (1292, "Incorrect datetime value: '2017-09-01T24:00:00Z' for ...
                    raise BadDBQuery

            if self._engine.closed:
                # 接続が切れた
                raise DatabaseConnectionLost
            else:
                # わからんけど失敗した
                raise DatabaseWriteFailed
        else:
            # update head
            self._message_heads[message_box.uuid] = message.primary_key

    def drop_message_box(self, message_box, connection=None):
        """MessageBox Tableを削除する.

        Args:
            message_box (circle_core.models.MessageBox): MessageBox
            connection (Optional[Connection]): Connection
        """
        if not connection:
            connection = self._engine.connect()

        table = self.find_table_for_message_box(message_box, create_if_not_exists=False)
        if table is not None:
            table.drop(self._engine)
            self._metadata.remove(table)
            del self._message_heads[message_box.uuid]

    # private?
    def _get_current_message_heads(self):
        connection = self._engine.connect()
        d = {}

        for box in MessageBox.query:
            key = None
            table = self.find_table_for_message_box(box, create_if_not_exists=False)
            if table is not None:
                query = (
                    sa.sql.select([table.c._created_at,
                                   table.c._counter]).order_by(table.c._created_at.desc(),
                                                               table.c._counter.desc()).limit(1)
                )
                rows = connection.execute(query).fetchall()

                if rows:
                    key = ModuleMessagePrimaryKey(ModuleMessage.make_timestamp(rows[0][0]), rows[0][1])

            d[box.uuid] = key

        connection.close()
        return d

    def connect(self):
        """Return a new Connection object.

        :return: Connection
        :rtype: Connection
        """
        try:
            return self._engine.connect()
        except sqlalchemy.exc.InterfaceError as exc:
            logger.exception('Failed to connect to database')
            raise DatabaseWriteFailed(exc)

    def make_table_for_message_box(self, message_box):
        """MessageBox Tableを生成する.

        Args:
            message_box (circle_core.models.MessageBox): MessageBox
        Returns:
            sa.Table: MessageBox Table
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
        columns.append(sa.PrimaryKeyConstraint('_created_at', '_counter'))
        kwargs = TABLE_OPTIONS.copy()
        # kwargs['autoload_with'] = self._engine
        table = sa.Table(table_name, self._metadata, *columns, **kwargs)

        # make table
        table.create(self._engine, checkfirst=True)

        return table

    def make_table_name_for_message_box(self, box_or_uuid):
        """MessageBox Table名を生成する.

        Args:
            box_or_uuid (Union[circle_core.models.MessageBox, uuid.UUID]):

        Returns:
            str:
        """
        if not isinstance(box_or_uuid, uuid.UUID):
            box_or_uuid = box_or_uuid.uuid

        encoded = b58encode(box_or_uuid.bytes)
        if isinstance(encoded, bytes):
            encoded = encoded.decode('latin1')

        return 'message_box_{}'.format(encoded)

    def find_table_for_message_box(self, message_box, create_if_not_exists=True):
        """MessageBox Tableを取得する.

        Args:
            message_box (circle_core.models.MessageBox): 取得するMessageBox
            create_if_not_exists (bool): Tableが存在しなければ作成する

        Returns:
            Optional[sa.Table]: MessageBox Table
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

    def _check_thread(self):
        """Threadの整合性をチェックする."""
        # TODO: ThreadPoolExecutorで動かすので、どのThreadで動くかわからないはず
        if self._thread_id is None:
            self._thread_id = threading.get_ident()
        # assert self._thread_id == threading.get_ident()

    def get_latest_primary_key(self, message_box):
        """get latest primary key.
        TODO: fill blank

        Args:
            message_box (circle_core.models.MessageBox): MessageBox
            connection (Optional[Connection]): Connection
        """
        pkey = self._message_heads.get(message_box.uuid)
        return pkey if pkey is not None else ModuleMessagePrimaryKey.origin()

    def count_messages(self, message_box, head=None, limit=None, connection=None):
        """メッセージ数を返す.

        Args:
            message_box (circle_core.models.MessageBox): MessageBox
            head (Optional[ModuleMessagePrimaryKey]): HEAD
            limit (Optional[int]): 取得数の上限
            connection (Optional[Connection]): Connection

        Returns:
            int: メッセージ数
        """
        if not connection:
            connection = self._engine.connect()

        table = self.find_table_for_message_box(message_box, create_if_not_exists=False)
        if table is None:
            return 0

        return connection.scalar(sa.sql.select([sa.func.count()]).select_from(table))

    def enum_messages(self, message_box, start=None, end=None, head=None, limit=None, order='asc', connection=None):
        """head以降のメッセージを返す.

        Args:
            message_box (circle_core.models.MessageBox): MessageBox
            start (Optional[float]): 開始日
            end (Optional[float]): 終了日
            head (Optional[ModuleMessagePrimaryKey]): HEAD
            limit (Optional[int]): 取得数の上限
            order (str): asc -> 古い順, desc -> 新しい順
            connection (Optional[Connection]): Connection
        Returns:
            Generator[ModuleMessage, ModuleMessage, ModuleMessage] メッセージジェネレータ
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

        Args:
            cycle_time (float):
            cycle_count (int):
        Returns:
            QueuedWriter: QueuedWriter
        """
        from .writer import JournalDBWriter, QueuedDBWriter, QueuedDBWriterDelegate

        # なぜここに書く必要があるのか?
        class Delegate(QueuedDBWriterDelegate):

            async def on_reconnect(self) -> None:
                jounal_writer.touch()  # type: ignore

        queued_writer = QueuedDBWriter(
            self, self._time_db_dir, cycle_time=cycle_time, cycle_count=cycle_count, delegate=Delegate()
        )
        jounal_writer = JournalDBWriter(queued_writer, self._log_dir)

        return jounal_writer

    # private
    def convert_payload(self, message_box: MessageBox, message: ModuleMessage) -> 'Dict[str, Any]':
        rv = {}
        for prop in message_box.schema.properties:
            if prop.type_val is None:
                raise ValueError('bad property')
            rv[prop.name] = convert_to_mysql_value(prop.type_val, message.payload[prop.name])
        return rv


def make_sqlcolumn_from_datatype(name, datatype):
    """schemaの型に応じて、SQLAlchemyのColumnを返す.

    Args:
        name (str): カラム名
        datatype (CRDataType): データ型
    Returns:
        sa.Column: カラム
    """

    assert not name.startswith('_')

    coltypes = {
        CRDataType.INT: sa.INTEGER,
        CRDataType.FLOAT: sa.FLOAT,
        CRDataType.BOOL: sa.BOOLEAN,
        CRDataType.STRING: sa.TEXT,
        CRDataType.BYTES: sa.TEXT,  # TODO: BLOBで保存するべきか？
        CRDataType.DATE: sa.DATE,
        CRDataType.DATETIME: sa.DATETIME,
        CRDataType.TIME: sa.TIME,
        CRDataType.TIMESTAMP: sa.TIMESTAMP,
        CRDataType.BLOB: sa.TEXT,
    }
    coltype = coltypes[CRDataType(datatype.upper())]()

    return sa.Column(name, coltype)


# to mysql value
def blob_to_mysql(value: 'StoredBlob') -> Any:
    return serialize(value)


def date_to_mysql(value: str) -> Any:
    if isinstance(value, str):
        if 'T' in value:
            value = value.split('T')[0]
            mo = DATE_REX.match(value)
            if mo:
                return datetime.date(int(mo.group(1), 10), int(mo.group(2), 10), int(mo.group(3), 10))

    dt = prepare_date(value)
    return dt.date()


def datetime_to_mysql(value: str) -> Any:
    dt = prepare_date(value)
    return dt


TO_MYSQLVALUE_MAP = {
    CRDataType.BLOB: blob_to_mysql,
    CRDataType.DATE: date_to_mysql,
    CRDataType.DATETIME: datetime_to_mysql,
}


def convert_to_mysql_value(datatype, value):
    """schemaの型に応じて、SQLAlchemyのColumnを返す.

    Args:
        name (str): カラム名
        datatype (CRDataType): データ型
    Returns:
        sa.Column: カラム
    """

    converter = TO_MYSQLVALUE_MAP.get(datatype, None)
    if converter:
        value = converter(value)

    return value
