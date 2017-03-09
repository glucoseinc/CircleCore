# -*- coding: utf-8 -*-

"""Metadata操作ログ."""

# system module
import functools

# community module
from sqlalchemy import event

# project module
from ..models import CcInfo, Invitation, MessageBox, Module, ReplicationLink, ReplicationMaster, Schema, User


# type annotation
try:
    from typing import Callable, List, Tuple, TYPE_CHECKING
    if TYPE_CHECKING:
        from sqlalchemy.engine import Connection
        from sqlalchemy.orm.mapper import Mapper
except ImportError:
    pass


MODELS = (CcInfo, Invitation, MessageBox, Module, ReplicationLink, ReplicationMaster, Schema, User)


class MetaDataEventListener(object):
    """MetaDataの変更を監視する.

    :param List[Tuple] listeners: イベントリスナー
    """
    def __init__(self):
        """init."""
        self.listeners = []

    def __del__(self):
        """del."""
        self.remove_all()

    def remove_all(self):
        """."""
        for args in self.listeners:
            event.remove(*args)
        self.listeners = []

    def on(self, model, before_or_after, handler):
        """イベントリスナーを登録する.

        :param str model: 対象のModel
        :param str before_or_after: 変更前か、変更後かを指定
        :param Callable handler: イベントハンドラ
        """
        assert before_or_after in ('before', 'after')
        if model in MODELS:
            pass
        else:
            model = model.lower()
            for klass in MODELS:
                if klass.__name__.lower() == model:
                    model = klass
                    break
            else:
                raise ValueError('invalid mode name `{}`'.format(model))

        for what in ('insert', 'update', 'delete'):
            identifier = '{}_{}'.format(before_or_after, what)
            fn = functools.partial(self.handle_event, identifier, handler)

            self.listeners.append((model, identifier, fn))
            event.listen(model, identifier, fn)

    def handle_event(self, what, handler, mapper, connection, target):
        """イベントハンドラ.

        :param str what: what
        :param Callable handler: handler
        :param Mapper mapper: mapper
        :param Connection connection: connection
        :param Any target: target
        """
        handler(what, target)
