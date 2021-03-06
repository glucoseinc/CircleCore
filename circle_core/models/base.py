# -*- coding: utf-8 -*-
"""Model Base."""

# system module
import uuid

# community module
from sqlalchemy import String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.types import CHAR, TypeDecorator

MetaDataSession = scoped_session(sessionmaker(autocommit=True, autoflush=False))


class MetaDataBase(declarative_base()):  # type: ignore
    """MetaData Base Model."""

    __abstract__ = True
    query = MetaDataSession.query_property()


class UUIDMetaDataBase(MetaDataBase):
    """UUIDを主キーとしたMetaData Base Model."""

    __abstract__ = True


def generate_uuid(model=None):
    """新しくUUIDを生成する.

    :param Any model: 渡されたら、このmodelの中で重複がないかチェックする
    """
    while True:
        new = uuid.uuid4()

        if model:
            check = model.query.filter_by(uuid=new).limit(1).all()
            if check:
                continue

        break
    return new


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
                # hex string
                return "%.32x" % value.int

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        else:
            return uuid.UUID(value)


class StrListBase(TypeDecorator):
    """Str List Base."""
    default_delimiter = ','

    def __init__(self, *arg, **kwargs):
        TypeDecorator.__init__(self, *arg, **kwargs)
        self.delimiter = kwargs.get('delimiter', self.default_delimiter)

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        elif isinstance(value, str):
            if self.delimiter in value:
                raise ValueError('value includs delimiter {!r}'.format(self.delimiter))
            return value
        # elif isinstance(value, (tuple, list)):
        elif hasattr(value, '__iter__'):
            for v in value:
                if self.delimiter in v:
                    raise ValueError('value includs delimiter {!r}'.format(self.delimiter))
            return self.delimiter.join(value)

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        else:
            return value.split(self.delimiter)


class StringList(StrListBase):
    """String List."""
    impl = String


class TextList(StrListBase):
    """Text List."""
    impl = Text
    default_delimiter = '\n'


class UUIDList(TypeDecorator):
    """UUIDList by Text."""
    impl = Text
    delimiter = ','

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        elif isinstance(value, str):
            if self.delimiter in value:
                raise ValueError('value includs delimiter {!r}'.format(self.delimiter))
            return value
        # elif isinstance(value, (tuple, list)):
        elif hasattr(value, '__iter__'):
            x = []
            for v in value:
                if isinstance(v, str):
                    if self.delimiter in v:
                        raise ValueError('value includs delimiter {!r}'.format(self.delimiter))
                    v = uuid.UUID(v)
                x.append(str(v))

            return self.delimiter.join(x)

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        else:
            return [uuid.UUID(x) for x in value.split(self.delimiter)]
