import asyncio
import functools
import glob
import json
import os
import typing
from typing import Optional, Tuple

from asyncio_extras import async_contextmanager

from typing_extensions import Protocol

from .base import DBWriter
from ..exceptions import JournalCorrupted, MessageBoxNotFoundError
from ..logger import logger
from ..message import ModuleMessage
from ..models import MessageBox, NoResultFound


class ChildWriteFailed(Exception):
    """child_writeにstoreできなかったときに呼ばれる. 内部用"""
    pass


class JournalReaderDelegate(Protocol):

    def on_advance_log_file(self, new_log_file_index: int) -> None:
        """新しいログファイルを開いた。

        (new_log_file_index - 1)まではいらなくなった"""

    pass


class JournalDBWriter(DBWriter, JournalReaderDelegate):
    """
    ジャーナルファイルに書き込んでから、子Writerに書き込むWriter
    """
    child_writer: DBWriter
    closed: bool
    journal_reader: 'JournalReader'
    journal_writer: 'JournalWriter'
    # storeになにか書き込まれたときに発火する。というかrunのloopを回したいときに発火する
    store_event: asyncio.Event
    prefix: str

    def __init__(self, child_writer, dirpath, *, file_prefix='journal', max_log_file_size=1024 * 1024):
        self.child_writer = child_writer
        self.prefix = os.path.join(dirpath, file_prefix)
        self.journal_reader, self.journal_writer = open_journal_reader_writer(
            self.prefix, max_log_file_size=max_log_file_size, delegate=self
        )
        self.closed = False
        self.store_event = asyncio.Event()
        self.writer_loop = asyncio.ensure_future(self.run())

    def __del__(self):
        if not self.closed:
            asyncio.get_event_loop().run_until_complete(self.close())

    # override
    async def store(self, message_box, message) -> bool:
        self.journal_writer.write(message.to_json(with_boxid=True))
        self.store_event.set()

        return True

    async def commit(self, flush_all=False):
        pass

    # delegate
    def on_advance_log_file(self, new_log_file_index: int) -> None:
        """new_log_file_index - 1までのファイルを消す"""
        log_files = list_log_files(self.prefix)

        logger.info('Log files is advanced to %d, rotating log files...', new_log_file_index)
        for index, filepath in log_files:
            if index < new_log_file_index:
                try:
                    os.unlink(filepath)
                    logger.info('remove old log file %s', filepath)
                except Exception:
                    logger.exception('Failed to remove old log file %s', filepath)

    # private
    async def close(self):
        if self.closed:
            logger.warning('Journal is already closed')
            return

        logger.info('close JournalDBWriter')
        self.closed = True
        self.store_event.set()
        await self.writer_loop

        self.journal_reader.close()
        self.journal_writer.close()

    async def run(self):
        """logファイルに新しいデータが書き込まれたら、child_writerに書込、posを進める"""
        assert not self.closed

        logger.debug('run started %r', self.closed)

        while not self.closed:
            try:
                async with self.journal_reader.read() as data:
                    logger.debug('Read message from log : %r', data)
                    if data:
                        rv = await self.store_message_to_child(data)
                        logger.debug('Store to child writer %r', rv)
                        if not rv:
                            raise ChildWriteFailed()

            except ChildWriteFailed:
                logger.debug('failed to write child writer. sleep 1 sec.')
                await asyncio.sleep(1)

            if data is None:
                # dataがなければ待つ
                logger.debug('Wait message...')
                self.store_event.clear()
                await self.store_event.wait()
                logger.debug('wakeup.')

        logger.debug('run finished')

    async def store_message_to_child(self, data: str) -> bool:
        parsed = json.loads(data)
        message_box = await self.find_message_box(parsed['boxId'])
        message = ModuleMessage.from_json(parsed)

        return await self.child_writer.store(message_box, message)

    @functools.lru_cache()
    async def find_message_box(self, box_id: str) -> MessageBox:
        # DBに直接触っちゃう
        try:
            box = MessageBox.query.filter_by(uuid=box_id).one()
        except NoResultFound:
            raise MessageBoxNotFoundError(box_id)

        return box


def open_journal_reader_writer(
    prefix: str, *, max_log_file_size: int = 1024 * 1024, delegate: Optional[JournalReaderDelegate] = None
) -> Tuple['JournalReader', 'JournalWriter']:
    """Journal Reader / Writerを作る"""
    log_files = list_log_files(prefix)

    #
    last_log_index, last_log_filepath = log_files[-1] if log_files else (None, None)

    reader = JournalReader(prefix, delegate=delegate)
    writer = JournalWriter(prefix, last_log_index or 0, max_log_file_size=max_log_file_size)

    return reader, writer
    # # load pos file
    # pos_file_path = os.path.join(self.dirpath, '{}.pos'.format(self.prefix))
    # pos_file_exists = os.path.exists(pos_file_path)
    # self.pos_file = open(pos_file_path, 'wt')

    # if pos_file_exists:
    #     if last_log_index is None:
    #         raise JournalCorrupted('log file not found')

    #     # load previous position
    #     try:
    #         data = open(pos_file_path, 'rt').read()
    #         self.write_position = [int(x, 10) for x in data.split('\n', 1)]
    #         logger.info('Open existing position %d:%d', index, position)
    #     except ValueError:
    #         pos_file_exists = False
    #     else:
    #         # write_positionから最新までのJournalがあるかチェック
    #         index = self.write_position[0]
    #         log_files_map = dict(log_files)
    #         while index <= last_log_index:
    #             if index not in log_files_map:
    #                 if last_log_index is None:
    #                     raise JournalCorrupted('log file {} not found'.format(index))


def list_log_files(prefix: str):
    log_files = []
    for fn in glob.iglob('{}.*'.format(prefix)):
        try:
            index = int(os.path.splitext(fn)[1][1:], 10)
        except ValueError:
            continue
        else:
            log_files.append((index, fn))
    log_files.sort()
    # log fileがそろっているか確認する
    if log_files:
        check = log_files[0][0]
        for idx, fn in log_files:
            if idx != check:
                raise JournalCorrupted('bad log file index')
            check += 1

    return log_files


class JournalWriter:
    prefix: str
    index: int
    log_file: Optional[typing.TextIO]
    max_log_file_size: int

    def __init__(self, prefix: str, index: int, *, max_log_file_size):
        self.prefix = prefix
        self.index = index
        self.log_file = None
        self.max_log_file_size = max_log_file_size

        self.prepare()

    def close(self):
        if self.log_file:
            self.log_file.close()
        self.log_file = None

    def write(self, message):
        # TODO: この部分をasyncにする???
        self.log_file.write(json.dumps(message, sort_keys=True))
        self.log_file.write('\n')
        self.log_file.flush()

        self.advance_log_file_if_needed()

    # private
    def prepare(self):
        assert self.log_file is None
        self.log_file = open(make_log_file_path(self.prefix, self.index), 'at')
        self.log_file.seek(0, os.SEEK_END)
        self.advance_log_file_if_needed()

    def advance_log_file_if_needed(self):
        assert self.log_file is not None

        log_file_size = self.log_file.tell()
        if log_file_size < self.max_log_file_size:
            return

        self.log_file.close()
        self.log_file = None
        self.index += 1

        path = make_log_file_path(self.prefix, self.index)
        if os.path.exists(path):
            raise JournalCorrupted('new log files is already exists: %s', path)
        self.log_file = open(path, 'xt')


def make_log_file_path(prefix: str, index: int):
    return '{}.{:03d}'.format(prefix, index)


class JournalReader:
    delegate: Optional[JournalReaderDelegate]
    log_file: Optional[typing.TextIO]
    log_file_index: Optional[int]
    pos_file: typing.TextIO
    prefix: str

    def __init__(self, prefix: str, *, delegate: Optional[JournalReaderDelegate] = None):
        self.prefix = prefix

        pos_file_path = '{}.pos'.format(self.prefix)
        self.pos_file = open(pos_file_path, 'r+t' if os.path.exists(pos_file_path) else 'w+t')
        self.position = self.read_position()
        logger.debug('load position %r', self.position)

        self.log_file = None
        self.log_file_index = None

        self.delegate = delegate

    def close(self):
        if self.log_file:
            self.log_file.close()
        self.log_file = None

        if self.pos_file:
            self.pos_file.close()
        self.pos_file = None

    @async_contextmanager
    async def read(self) -> None:
        if not self.log_file:
            if not self.log_file_index:
                self.log_file_index = self.position[0]

            log_file_path = make_log_file_path(self.prefix, self.log_file_index)
            if not os.path.exists(log_file_path):
                # ファイルがない -> まだログが無い
                logger.info('no log file opened, and log file not found')
                yield None
                return

            logger.info('open log file %s', log_file_path)

            self.log_file = open(log_file_path)
            self.log_file.seek(self.position[1], os.SEEK_SET)

            # check file size
            stat = os.stat(log_file_path)
            if stat.st_size < self.position[1]:
                # ファイルサイズが足りない
                raise JournalCorrupted('bad position or log file size')

            # tellでファイルサイズを調べてはいけない
            # if self.log_file.tell() != self.position[1]:

        # 1行読み取る のだが、ページめくる処理も.
        while True:
            saved_position = self.log_file.tell()
            logger.debug('read from %r / pos %r', saved_position, self.position)
            ln = self.log_file.readline()
            if ln:
                break

            # 読み取れなかった場合、次のlogがあるか確認
            next_log_file_path = make_log_file_path(self.prefix, self.log_file_index + 1)
            if not os.path.exists(next_log_file_path):
                # 次のファイルもないので、単純にログがない
                logger.info('log tail reached, and no following log file')
                yield None
                return

            self.log_file = open(next_log_file_path)
            self.log_file_index += 1

            if self.delegate:
                self.delegate.on_advance_log_file(self.log_file_index)

        # yield
        try:
            yield ln
        except Exception:
            # 再度同じものが読めるように巻き戻す
            self.log_file.seek(saved_position, os.SEEK_SET)
            raise
        else:
            # write position
            self.position = self.log_file_index, self.log_file.tell()
            logger.debug('new pos %r', self.position)
            await self.write_position()

    # private
    def read_position(self):
        self.pos_file.seek(0, os.SEEK_SET)
        data = self.pos_file.read()
        logger.debug('read_position %r', data)
        if not data:
            # initial
            return 0, 0

        index, position = [int(x, 10) for x in data.split('\n', 1)]
        return index, position

    async def write_position(self):
        self.pos_file.seek(0, os.SEEK_SET)
        self.pos_file.write('{}\n{}'.format(*self.position))
        self.pos_file.flush()
        logger.debug('write pos %r', self.position)
