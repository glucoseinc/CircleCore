# -*- coding: utf-8 -*-
"""
Metadata操作ログ
"""
import functools
from sqlalchemy import event

from ..models import CcInfo, Invitation, MessageBox, Module, ReplicationLink, Schema, User


MODELS = (CcInfo, Invitation, MessageBox, Module, ReplicationLink, Schema, User)


class MetaDataEventListener(object):
    """
    """
    def __init__(self):
        self.listeners = []

    def __del__(self):
        self.remove_all()

    def remove_all(self):
        for args in self.listeners:
            event.remove(*args)
        self.listeners = []

    def on(self, model, before_or_after, handler):
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
        handler(what, target)
