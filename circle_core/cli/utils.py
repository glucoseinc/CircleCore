# -*- coding: utf-8 -*-

"""CLI Utilities."""

# system module
from itertools import cycle
from multiprocessing import Process
from signal import SIGINT, signal, SIGTERM
from time import sleep, time
from unicodedata import east_asian_width
from uuid import uuid4

# community module
import click
from six import PY2, PY3
from six.moves import zip_longest

if PY3:
    from typing import List, Optional, Tuple


def output_listing_columns(data, header):
    """データリストを整形し表示する.

    :param List[List[str]] data: データリスト
    :param List[str] header: 見出し
    """
    if len(data) > 0:
        data.insert(0, header)

    row_strings, sizes = create_row_strings(data)

    # Create and add a separator.
    if len(data) > 0:
        separator = ' '.join(['-' * size for size in sizes])
        row_strings.insert(1, separator)

    # Display rows.
    for row_string in row_strings:
        click.echo(row_string)


def output_properties(data):
    """プロパティリストを整形し表示する.

    :param List[Tuple[str, str]] data: プロパティリスト
    """
    data = [[datum[0], ':', datum[1]] for datum in data]
    row_strings, _ = create_row_strings(data)

    # Display rows.
    for row_string in row_strings:
        click.echo(row_string)


def create_row_strings(rows):
    """テーブルデータを表示用に整形する.

    :param List[List[str]] rows: テーブルデータ
    :return: row_strings: 表示用に整形したテーブルデータ, sizes: 各カラムの文字列長
    :rtype: Tuple[List[str], List[int]]
    """
    def _len(string):
        """文字列長を計算する.

        ワイド文字と判断できる文字は2カウントする.

        :param str string: 対象文字列
        :return: 文字列長
        :rtype: int
        """
        if PY2:
            string = string.decode('utf-8')
        return sum([1 if 'NaH'.count(east_asian_width(char)) > 0 else 2
                    for char in string])

    def _ljust(size, string):
        """文字列の右にパディングを付与する.

        :param int size: パディング付与後の文字列長
        :param str string: 対象文字列
        :return: パディング付与後の文字列
        :rtype: str
        """
        return string + ' ' * (size - _len(string))

    assert len(rows) > 0

    # Calculate columns size.
    sizes = [0] * max(len(x) for x in rows)
    for row in rows:
        sizes = [max(size, _len(string)) for size, string in zip_longest(sizes, row)]

    # Create row strings.
    row_strings = []
    for row in rows:
        row_string = ' '.join([_ljust(size, string) if string is not None else ''
                               for size, string in zip_longest(sizes, row)])
        row_strings.append(row_string)

    return row_strings, sizes


def generate_uuid(existing=None):
    """UUIDを生成する.

    :param Optional[List[str]] existing: 使用中のUUIDリスト
    :return: UUID
    :rtype: str
    """
    generated = str(uuid4())
    if existing is not None:
        while generated in existing:
            generated = str(uuid4())
    return generated


class RestartableProcess:
    """RestartableProcess.

    :param list args:
    :param dict kwargs:
    :param int startedTime:
    :param Process proc:
    :param list procs:
    """

    procs = []

    @classmethod
    def wait_all(cls):
        """`crcr run`."""
        signal(SIGTERM, cls.terminate_all)
        signal(SIGINT, cls.terminate_all)

        for proc in cycle(cls.procs):
            proc.join(0.1)
            if not proc.is_alive():
                click.echo('PID {} has died. Restarting...'.format(proc.pid))
                try:
                    proc.start()
                except RuntimeError:
                    cls.terminate_all()

    @classmethod
    def terminate_all(cls, *args):
        """全ての子プロセスをterminate."""
        for proc in cls.procs:
            proc.terminate()

        click.get_current_context().abort()

    def __init__(self, *args, **kwargs):
        """constructor."""
        self.args = args
        self.kwargs = kwargs
        self.startedTime = 0

    def __getattr__(self, attr):
        """delegation."""
        return getattr(self.proc, attr)

    def start(self):
        """start."""
        if 10 > time() - self.startedTime:
            raise RuntimeError('Restarted process has died immediately')

        self.proc = Process(*self.args, **self.kwargs)
        self.procs.append(self)
        self.proc.daemon = True
        self.proc.start()
        self.startedTime = time()
