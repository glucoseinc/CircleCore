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


@enum.unique
class RequestType(enum.Enum):
    # 新しいメッセージを登録したい
    NEW_MESSAGE = 'new_message'


@enum.unique
class ReplicationState(enum.Enum):
    """
    ReplicationのStateを表す
    """

    # 初期状態
    HANDSHAKING = 'handshaking'
    MIGRATING = 'migrating'
    SYNCING = 'syncing'


@enum.unique
class SlaveCommand(enum.Enum):
    """
    Slaveから送られてくるコマンド
    """

    HELLO = 'hello'
    MIGRATED = 'migrated'

    FAILURE = 'failure'


@enum.unique
class MasterCommand(enum.Enum):
    """
    Masterから送るコマンド
    """

    MIGRATE = 'migrate'
    SYNC_MESSAGE = 'sync_message'
    NEW_MESSAGE = 'new_message'


@enum.unique
class WebsocketStatusCode(enum.Enum):
    CLOSE_NORMALY = 1000
    GOING_AWAY = 1001
    PROTOCOL_ERROR = 1002
    DATA_CANNOT_ACCEPT = 1003
    VIOLATE_POLICY = 1008
    MESSAGE_IS_TOO_BIG = 1009
