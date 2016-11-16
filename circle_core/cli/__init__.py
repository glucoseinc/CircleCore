#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .cli_main import cli_main
from .device import cli_device

cli_main.add_command(cli_device, 'device')
