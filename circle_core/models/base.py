# -*- coding: utf-8 -*-

"""Model Base."""

# system module
import re
import uuid
from uuid import UUID

# community module
from six import PY3
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.types import CHAR, TypeDecorator
# from sqlalchemy.dialects.postgresql import UUID

if PY3:
    from typing import Union


MetaDataSession = scoped_session(sessionmaker(autocommit=True, autoflush=False))


class MetaDataBase(declarative_base()):
    __abstract__ = True
    query = MetaDataSession.query_property()


def generate_uuid(model=None):
    """新しくUUIDを生成する

    :param class model: 渡されたら、このmodelの中で重複がないかチェックする
    """
    while True:
        new = uuid.uuid4()

        if model:
            check = model.query.filter_by(uuid=new).limit(1).all()
            if check:
                continue

        break
    return new


class UUIDBasedObject(object):
    """UUIDを持つ基底オブジェクト.
    :param str key_prefix: ストレージキーのプレフィックス
    :param UUID uuid: Object UUID
    """

    key_prefix = ''

    def __init__(self, uuid):
        """init.

        :param Union[str, UUID] uuid: User UUID
        """
        if uuid and not isinstance(uuid, UUID):
            try:
                uuid = UUID(uuid)
            except ValueError:
                raise ValueError('Invalid uuid : {}'.format(uuid))

        self.uuid = uuid

    @classmethod
    def make_storage_key(cls, uuid):
        """ストレージキーを作成する.

        :param UUID uuid: UUID
        :return: ストレージキー
        :rtype: str
        """
        return '{}_{}'.format(cls.key_prefix, uuid)

    @property
    def storage_key(self):
        """ストレージキー.

        :return: ストレージキー
        :rtype: str
        """
        return self.make_storage_key(self.uuid)

    @classmethod
    def is_key_matched(cls, key):
        """指定のキーがストレージキーの形式にマッチしているか.

        :param str key:
        :return: マッチしているか
        :rtype: bool
        """
        pattern = '^{}_{}'.format(
            cls.key_prefix,
            r'[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$'
        )
        return re.match(pattern, key) is not None


class GUID(TypeDecorator):
    """Platform-independent GUID type.

    Uses PostgreSQL's UUID type, otherwise uses
    CHAR(32), storing as stringified hex values.

    """
    impl = CHAR

    def load_dialect_impl(self, dialect):
        if dialect.name == 'postgresql':
            return dialect.type_descriptor(UUID())
        else:
            return dialect.type_descriptor(CHAR(32))

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        elif dialect.name == 'postgresql':
            return str(value)
        else:
            if not isinstance(value, uuid.UUID):
                return "%.32x" % uuid.UUID(value).int
            else:
                # hexstring
                return "%.32x" % value.int

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        else:
            return uuid.UUID(value)
