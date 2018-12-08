# -*- coding: utf-8 -*-
"""workers. invoked by `crcr worker run <module_name>`."""
import abc
import typing
import weakref

if typing.TYPE_CHECKING:
    from cirlce_core.app import CircleCore


WorkerType = typing.NewType('WorkerType', str)
WorkerKey = typing.NewType('WorkerKey', str)
WorkerConfig = typing.Mapping[str, typing.Any]
WorkerFactory = typing.Callable[['CircleCore', WorkerType, WorkerKey, WorkerConfig], 'CircleWorker']

worker_factories: typing.Dict[WorkerKey, WorkerFactory] = {}


def register_worker_factory(type):
    def _f(f):
        if type in worker_factories:
            raise ValueError('type {} is already registered')
        worker_factories[type] = f
    return _f


def make_worker(core, type, key, config):
    return worker_factories[type](core, type, key, config)


class CircleWorker(metaclass=abc.ABCMeta):
    worker_type: WorkerType

    def __init__(self, core, worker_key):
        self.core = weakref.proxy(core)
        self.worker_key = worker_key

    @abc.abstractmethod
    def initialize(self):
        pass

    @abc.abstractmethod
    def finalize(self):
        pass
