# -*- coding: utf-8 -*-
from __future__ import absolute_import


class CircleCoreException(Exception):
    """CircleCoreの例外全般の基底クラス"""
    pass


class DatabaseMismatchError(CircleCoreException):
    """Databaseとスキーマが整合しない場合の例外"""
    pass


class MigrationError(CircleCoreException):
    """Databaseのマイグレーションに失敗した時の例外"""
    pass


class ModuleNotFoundError(CircleCoreException):
    """Moduleが見つからない時の例外"""
    pass


class SchemaNotFoundError(CircleCoreException):
    """Schemaが見つからない時の例外"""
    pass
