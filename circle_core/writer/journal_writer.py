import glob
import json
import os

from .base import WriterBase
from ..exceptions import JournalCorrupted
from ..logger import logger


class JournalWriter(WriterBase):
    """
    ジャーナルファイルに書き込んでから、子Writerに書き込むWriter
    """

    def __init__(self, child_writer, dirpath, *, prefix='journal', max_log_file_size=1024 * 1024):
        self.child_writer = child_writer
        self.dirpath = dirpath
        self.prefix = prefix

        # どこまでchild_writerに書き込んだかが入るファイル
        self.pos_file = None
        # メッセージが追記されていくファイル
        self.log_file = None
        # どこまで書いたか。常にpos_fileと同じ値になるはず (index, position)
        self.write_position = None
        self.prepare()

        self.max_log_file_size = max_log_file_size

    def __del__(self):
        if self.pos_file:
            self.pos_file.close()
        if self.journal_file:
            self.journal_file.close()

    # override
    def store(self, message_box, message):
        self.log_file.write(json.dumps(message.to_json(with_boxid=True)))
        self.log_file.write('\n')
        self.log_file.flush()
        log_file_size = self.log_file.tell()

        if log_file_size >= self.max_log_file_size:
            self.rotate_logs()

    def commit(self, flush_all=False):
        pass

    # private
    def make_log_file_path(self, index):
        return os.path.join(self.dirpath, '{}.{:03d}'.format(self.prefix, index))

    def prepare(self):
        # find last journal file
        log_files = []
        for fn in glob.iglob(os.path.join(self.dirpath, '{}.*'.format(self.prefix))):
            try:
                index = int(os.path.splitext(fn)[1][1:], 10)
            except ValueError:
                continue
            else:
                log_files.append((index, log_files))
        log_files.sort()
        last_log_index, last_log_filepath = journal_files[-1] if log_files else (None, None)

        # load pos file
        pos_file_path = os.path.join(self.dirpath, '{}.pos'.format(self.prefix))
        pos_file_exists = os.path.exists(pos_file_path)
        self.pos_file = open(pos_file_path, 'wt')

        if pos_file_exists:
            if last_journal_index is None:
                raise JournalCorrupted('journal file not found')

            # load previous position
            data = open(pos_file_path, 'rt').read()
            self.write_position = [int(x, 10) for x in data.split('\n', 1)]
            logger.info('Open existing journal %d:%d', index, position)

            # write_positionから最新までのJournalがあるかチェック
            index = self.write_position[0]
            log_files_map = dict(log_files)
            while index <= last_log_index:
                if index not in log_files_map:
                    if last_log_index is None:
                        raise JournalCorrupted('journal file {} not found'.format(index))
        else:
            # create new position file
            logger.info('Create new journal position file')
            self.write_position = 0, 0
            self.store_position()

        # open last journal file
        if last_log_index is None:
            last_log_index = 0
        self.log_file = open(self.make_log_file_path(last_log_index), 'at')

    def store_position(self):
        self.pos_file.seek(0, os.SEEK_SET)
        self.pos_file.write('{}\n{}'.format(*self.write_position))
        self.pos_file.flush()

    def rotate_logs(self):
        assert 0
