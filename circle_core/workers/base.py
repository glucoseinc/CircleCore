# -*- coding: utf-8 -*-
"""workers. invoked by `crcr worker run <module_name>`."""
import abc
import typing
import weakref
from typing import Any, Callable, Mapping, NewType, TYPE_CHECKING

if TYPE_CHECKING:
    from cirlce_core.app import CircleCore  # noqa

WorkerType = NewType('WorkerType', str)
WorkerKey = NewType('WorkerKey', str)
WorkerConfig = Mapping[str, Any]
WorkerFactory = Callable[['CircleCore', WorkerType, WorkerKey, WorkerConfig], 'CircleWorker']

worker_factories: typing.Dict[WorkerType, WorkerFactory] = {}


def register_worker_factory(type):

    def _f(f):
        if type in worker_factories:
            raise ValueError('type {} is already registered')
        worker_factories[type] = f

    return _f


def make_worker(core: 'CircleCore', type: WorkerType, key: WorkerKey, config: WorkerConfig) -> 'CircleWorker':
    return worker_factories[type](core, type, key, config)


class CircleWorker(metaclass=abc.ABCMeta):
    worker_type: WorkerType

    def __init__(self, core, worker_key):
        self.core = weakref.proxy(core)
        self.worker_key = worker_key

    def initialize(self):
        pass

    def finalize(self):
        pass
