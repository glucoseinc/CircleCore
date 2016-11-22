#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""標準出力へのlogger."""
from logging import DEBUG, getLogger, StreamHandler
from sys import stdout


logger = getLogger('circle_core')
logger.setLevel(DEBUG)
stream = StreamHandler(stdout)
stream.setLevel(DEBUG)
logger.addHandler(stream)
