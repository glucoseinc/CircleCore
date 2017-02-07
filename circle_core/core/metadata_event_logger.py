# -*- coding: utf-8 -*-
"""
Metadata操作ログ
"""
import collections
from sqlalchemy import event, inspect

import click

from . import logger
from ..models import CcInfo, Invitation, MessageBox, Module, ReplicationLink, Schema, User


MODELS = (CcInfo, Invitation, MessageBox, Module, ReplicationLink, Schema, User)


def get_current_user():
    # flaskかな?
    from flask.globals import _request_ctx_stack

    if _request_ctx_stack.top:
        from flask import g, request
        from circle_core.server.wui.authorize import oauth

        if hasattr(g, 'user'):
            return '{}@web'.format(g.user.uuid)
        if hasattr(request, 'oauth'):
            return '{}@api'.format(request.oauth.user.uuid)
        else:
            valid, req = oauth.verify_request([])
            return '{}@api'.format(req.user.uuid)

    # cliかな?
    if click.get_current_context():
        return '@cli'


class MetaDataEventLogger(object):
    """
    """
    def __init__(self, core, log_file_path):
        self._install()

        self.log_file = open(log_file_path, 'a')

    def _install(self):
        logger.debug('Installing metadata event handlers.')
        for model in MODELS:
            for what in ('before_insert', 'before_update', 'before_delete'):
                event.listen(
                    model,
                    what,
                    getattr(self, 'on_' + what)
                )

    def on_before_insert(self, mapper, connection, target):
        self.log('insert', target, uuid=target.uuid, data=target.to_json())

    def on_before_update(self, mapper, connection, target):
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

    def on_before_delete(self, mapper, connection, target):
        self.log('delete', target, uuid=target.uuid)

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
