# -*- coding: utf-8 -*-
"""workers. invoked by `crcr worker run <module_name>`."""
import weakref

worker_factories = {}


def register_worker_factory(type):
    def _f(f):
        if type in worker_factories:
            raise ValueError('type {} is already registered')
        worker_factories[type] = f
    return _f


def make_worker(core, type, key, config):
    return worker_factories[type](core, type, key, config)


class CircleWorker(object):
    worker_type = None

    def __init__(self, core, worker_key):
        self.core = weakref.proxy(core)
        self.worker_key = worker_key

    def initialize(self):
        pass

    def finalize(self):
        pass
