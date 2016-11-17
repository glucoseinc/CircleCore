#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""CLI Utilities."""

# system module
from unicodedata import east_asian_width

# community module
import click
from six import PY2


if PY2:
    from itertools import izip_longest as zip_longest
else:
    from itertools import zip_longest
    from typing import Dict, List, Tuple


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


def create_row_strings(rows):
    """テーブルデータを表示用に整形する.

    :param List[List[str]] rows: テーブルデータ
    :return: row_strings: 表示用に整形したテーブルデータ, sizes: 各カラムの文字列長
    :rtype: Tuple[List[str], int]
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


def stringify_dict(dic):
    """辞書を文字列に変換する.

    :param dic: 対象辞書
    :type dic: Dict[str, Any]
    :return: 変換後の文字列
    :rtype: str
    """
    items = []
    for k, v in dic.items():
        items.append('{}:{}'.format(k, v))
    return ', '.join(items)