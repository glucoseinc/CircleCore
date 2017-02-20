# -*- coding: utf-8 -*-
from __future__ import absolute_import

import enum


@enum.unique
class CRDataType(enum.Enum):
    """メッセージスキーマのプロパティの型."""

    INT = 'INT'
    FLOAT = 'FLOAT'
    BOOL = 'BOOL'
    STRING = 'STRING'
    BYTES = 'BYTES'
    DATE = 'DATE'
    DATETIME = 'DATETIME'
    TIME = 'TIME'
    TIMESTAMP = 'TIMESTAMP'


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
