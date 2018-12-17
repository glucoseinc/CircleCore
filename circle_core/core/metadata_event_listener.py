# -*- coding: utf-8 -*-
"""Metadata操作ログ."""

# system module
import functools
from typing import Any, Callable, List, TYPE_CHECKING, Tuple, Union, cast

# community module
from sqlalchemy import event

# project module
from ..models import CcInfo, Invitation, MessageBox, Module, ReplicationLink, ReplicationMaster, Schema, User

# type annotation

if TYPE_CHECKING:
    from sqlalchemy.engine import Connection
    from sqlalchemy.orm.mapper import Mapper

MODELS = (CcInfo, Invitation, MessageBox, Module, ReplicationLink, ReplicationMaster, Schema, User)
EventHandler = Callable[[str, Any], None]


class MetaDataEventListener(object):
    """MetaDataの変更を監視する.

    :param List[Tuple] listeners: イベントリスナー
    """
    listeners: List[Tuple[type, str, Callable[..., Any]]]

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

    def on(self, model: Union[str, type], before_or_after: str, handler: EventHandler) -> None:
        """イベントリスナーを登録する.

        Args:
            model: 対象のModel
            before_or_after: 変更前か、変更後かを指定
            handler: イベントハンドラ
        """
        assert before_or_after in ('before', 'after')
        model_class: type
        if model in MODELS:
            model_class = cast(type, model)
        elif isinstance(model, str):
            model = model.lower()
            for klass in MODELS:
                if klass.__name__.lower() == model:
                    model_class = klass
                    break
            else:
                raise ValueError('invalid model name `{}`'.format(model))

        for what in ('insert', 'update', 'delete'):
            identifier = '{}_{}'.format(before_or_after, what)
            fn = cast(Callable[..., Any], functools.partial(self.handle_event, identifier, handler))

            self.listeners.append((model_class, identifier, fn))
            event.listen(model_class, identifier, fn)

    def handle_event(
        self, what: str, handler: EventHandler, mapper: 'Mapper', connection: 'Connection', target: Any
    ) -> None:
        """イベントハンドラ.

        :param str what: what
        :param Callable handler: handler
        :param Mapper mapper: mapper
        :param Connection connection: connection
        :param Any target: target
        """
        handler(what, target)
