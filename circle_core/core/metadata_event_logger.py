# -*- coding: utf-8 -*-
"""
Metadata操作ログ
"""
import collections

import click
from sqlalchemy import inspect

from circle_core import models
from circle_core.models import User
from circle_core.models.base import UUIDMetaDataBase
from .base import logger
from .metadata_event_listener import MetaDataEventListener


def get_current_user():
    # flaskかな?
    from flask.globals import _request_ctx_stack

    if _request_ctx_stack.top:
        from flask import g, request
        from circle_core.web.authorize import oauth

        if hasattr(g, 'user'):
            return '{}@web'.format(g.user.uuid)
        if hasattr(request, 'oauth'):
            return '{}@api'.format(request.oauth.user.uuid)
        else:
            valid, req = oauth.verify_request([])
            if req.user:
                return '{}@api'.format(req.user.uuid)

            return 'public@web'

    # cliかな?
    if click.get_current_context():
        return '@cli'


class MetaDataEventLogger(object):
    """
    """
    def __init__(self, core, log_file_path):
        self.listener = MetaDataEventListener()
        self.log_file = open(log_file_path, 'a')

        self._install()

    def _install(self):
        logger.debug('Installing metadata event handlers.')

        for key in dir(models):
            klass = getattr(models, key)
            try:
                if klass != UUIDMetaDataBase and issubclass(klass, UUIDMetaDataBase):
                    self.listener.on(klass.__name__, 'before', self.handle_metadata_event)
            except TypeError:
                pass

    def handle_metadata_event(self, what, target):
        if what == 'before_insert':
            self.log('insert', target, uuid=target.uuid, data=target.to_json())
        elif what == 'before_delete':
            self.log('delete', target, uuid=target.uuid)
        elif what == 'before_update':
            # get diffs
            diff = []

            # がんばってdiffをとっているけどSQLAlchemyの仕様がよくわからない
            for key, attr in inspect(target).attrs.items():
                hist = attr.history
                # 普通の属性が変更された場合はこれでいける
                if hist.added and not hist.unchanged:
                    # key, before, after
                    if hist.added != hist.deleted:
                        diff.append({
                            'key': key,
                            'before': hist.deleted,
                            'after': hist.added,
                        })
                elif hist.unchanged and not hist.added and not hist.deleted:
                    # unchanged attr
                    pass
                elif not hist.unchanged and not hist.added and not hist.deleted:
                    # unchanged relation
                    pass
                else:
                    logger.debug('%r: unhandled diff: %s %r', target, key, hist)

            # Userの更新日の処理はスキップする
            if isinstance(target, User) and len(diff) == 1 and diff[0]['key'] == 'last_access_at':
                return
            if not diff:
                return

            self.log('update', target, diff=diff)

    def log(self, what, instance, **details):
        data = collections.OrderedDict()
        data['user'] = get_current_user()
        data['what'] = what
        data['table'] = instance.__tablename__
        for key, val in details.items():
            data[key] = val

        # pack to ltsv
        ltsv = '\t'.join('{}:{}'.format(key, val) for key, val in data.items())
        logger.debug('log > %s', ltsv)

        self.log_file.write(ltsv)
        self.log_file.write('\n')
        self.log_file.flush()
