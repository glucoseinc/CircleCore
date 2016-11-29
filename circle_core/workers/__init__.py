# -*- coding: utf-8 -*-
"""workers. invoked by `crcr worker run <module_name>`."""
from importlib import import_module

from circle_core.helpers import logger
from click import get_current_context


def get_worker(worker_name):
    """ワーカーを返す.

    :param str worker_name:
    :return FunctionType:
    """
    try:
        worker = import_module('circle_core.workers.' + worker_name)
    except ImportError:
        get_current_context().fail('worker %r is not found' % worker_name)
    else:
        return worker
