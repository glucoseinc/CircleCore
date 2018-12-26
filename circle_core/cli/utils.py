# -*- coding: utf-8 -*-
"""CLI Utilities."""

# system module
from itertools import zip_longest
from typing import TYPE_CHECKING
from unicodedata import east_asian_width
from uuid import UUID

# community module
import click

if TYPE_CHECKING:
    from typing import Any, List, Tuple

    TableHeader = List[str]
    TableData = List[Tuple[Any, ...]]


def output_listing_columns(data: 'TableData', header: 'TableHeader'):
    """データリストを整形し表示する.

    Args:
        data: データリスト
        header: 見出し
    """
    if len(data) > 0:
        data.insert(0, tuple(header))

    row_strings, sizes = create_row_strings(data)

    # Create and add a separator.
    if len(data) > 0:
        separator = ' '.join(['-' * size for size in sizes])
        row_strings.insert(1, separator)

    # Display rows.
    for row_string in row_strings:
        click.echo(row_string)


def output_properties(data: 'List[Tuple[str, str]]'):
    """プロパティリストを整形し表示する.

    :param List[Tuple[str, str]] data: プロパティリスト
    """
    row_strings, _ = create_row_strings([[l, ':', r] for l, r in data])

    # Display rows.
    for row_string in row_strings:
        click.echo(row_string)


def create_row_strings(rows) -> 'Tuple[List[str], List[int]]':
    """テーブルデータを表示用に整形する.

    :param List[List[str]] rows: テーブルデータ
    :return: row_strings: 表示用に整形したテーブルデータ, sizes: 各カラムの文字列長
    :rtype: Tuple[List[str], List[int]]
    """

    def _len(string: str) -> int:
        """文字列長を計算する.

        ワイド文字と判断できる文字は2カウントする.

        :param str string: 対象文字列
        :return: 文字列長
        :rtype: int
        """
        return sum([1 if 'NaH'.count(east_asian_width(char)) > 0 else 2 for char in string])

    def _ljust(size: int, string: str) -> str:
        """文字列の右にパディングを付与する.

        :param int size: パディング付与後の文字列長
        :param str string: 対象文字列
        :return: パディング付与後の文字列
        :rtype: str
        """
        return string + ' ' * (size - _len(string))

    assert len(rows) > 0

    # 全てstrに変換
    rows = [[str(c) for c in row] for row in rows]

    # Calculate columns size.
    sizes = [0] * max(len(x) for x in rows)
    for row in rows:
        sizes = [max(size, _len(string)) for size, string in zip_longest(sizes, row)]

    # Create row strings.
    row_strings = []
    for row in rows:
        row_string = ' '.join(
            [_ljust(size, string) if string is not None else '' for size, string in zip_longest(sizes, row)]
        )
        row_strings.append(row_string)

    return row_strings, sizes


def convert_stringified_uuid_list(ctx, param, value):
    """カンマ区切りUUIDを、List[uuid.UUID]に変換"""
    if value is None:
        return value

    print(value)
    try:
        return list(UUID(x) for x in value.split(','))
    except ValueError as exc:
        raise click.BadParameter('bad uuid list {!r}'.format(exc))
