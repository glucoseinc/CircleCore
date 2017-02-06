# -*- coding: utf-8 -*-
"""workers. invoked by `crcr worker run <module_name>`."""


from .base import make_worker
from . import (
    datareceiver,
#     normalizer,
)


WORKER_DATARECEIVER = datareceiver.WORKER_DATARECEIVER
# WORKER_NORMALIZER = normalizer.WORKER_NORMALIZER
