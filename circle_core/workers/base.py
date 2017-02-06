# -*- coding: utf-8 -*-
"""workers. invoked by `crcr worker run <module_name>`."""
import weakref

worker_factories = {}


def register_worker_factory(type, factory):
    if type in worker_factories:
        raise ValueError('type {} is already registered')

    worker_factories[type] = factory


def make_worker(core, type, key, config):
    return worker_factories[type](core, type, key, config)


class CircleWorker(object):
    def __init__(self, core):
        self.core = weakref.ref(core)

    def run(self):
        raise NotImplementedError
