# -*- coding: utf-8 -*-
from __future__ import absolute_import

import enum


class CRDataType(enum.Enum):
    """
    センサーデータのパラメータの型を定義する
    """
    INT = 1
    FLOAT = 2
    TEXT = 3

    def to_text(self):
        """
        センサデータ型を、対応するテキスト表現に変換する

        :return str: センサデータ型名
        """
        return DATATYPE_TO_TEXT_MAP[self]

    @classmethod
    def from_text(cls, text):
        """
        テキスト表現からセンサー型を返す

        :param str text: センサデータ型名
        :return CRDataType: センサーデータ型
        """
        return DATATYPE_FROM_TEXT_MAP[text]


DATATYPE_TO_TEXT_MAP = {
    CRDataType.INT: 'int',
    CRDataType.FLOAT: 'float',
    CRDataType.TEXT: 'text',
}
DATATYPE_FROM_TEXT_MAP = dict(((v, k) for k, v in DATATYPE_TO_TEXT_MAP.items()))


@enum.unique
class CRScope(enum.Enum):
    """
    circle_core APIのscopeを定義する
    """
    # ユーザ情報の読み込み
    USER_R = 'user+r'
    # ユーザ情報の管理
    USER_RW = 'user+rw'
    # モジュール、メッセージスキーマなどを閲覧するだけ
    SCHEMA_R = 'schema+r'
    # モジュール、メッセージスキーマなどの管理
    SCHEMA_RW = 'schema+rw'
