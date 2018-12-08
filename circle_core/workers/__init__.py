# -*- coding: utf-8 -*-
"""workers. invoked by `crcr worker run <module_name>`."""

from . import (datareceiver, http, slave_driver)
from .base import make_worker

WORKER_DATARECEIVER = datareceiver.WORKER_DATARECEIVER
WORKER_SLAVE_DRIVER = slave_driver.WORKER_SLAVE_DRIVER
