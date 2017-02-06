# -*- coding: utf-8 -*-
"""workers. invoked by `crcr worker run <module_name>`."""


from . import (
    datareceiver,
    http,
)
from .base import make_worker


WORKER_DATARECEIVER = datareceiver.WORKER_DATARECEIVER
