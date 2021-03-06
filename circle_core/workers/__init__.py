# -*- coding: utf-8 -*-
"""workers. invoked by `crcr worker run <module_name>`."""

import typing

from . import (datareceiver, http, slave_driver)  # noqa
from .base import CircleWorker, make_worker
from .blobstore import BlobStoreWorker, WORKER_BLOBSTORE

WORKER_DATARECEIVER = datareceiver.WORKER_DATARECEIVER
WORKER_SLAVE_DRIVER = slave_driver.WORKER_SLAVE_DRIVER

__all__ = (
    'CircleWorker',
    'make_worker',
    'BlobStoreWorker',
    'WORKER_DATARECEIVER',
    'WORKER_SLAVE_DRIVER',
    'WORKER_BLOBSTORE',
)

if typing.TYPE_CHECKING:
    from .base import WorkerConfig, WorkerKey, WorkerType

    __all__ += ('WorkerConfig', 'WorkerType', 'WorkerKey')  # type: ignore
