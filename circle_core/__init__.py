# -*- coding: utf-8 -*-
"""CircleCore."""
import sys
from logging import basicConfig, StreamHandler, DEBUG, Formatter


basicConfig(format='%(levelname)s:%(name)s - %(message)s', level=DEBUG, stream=sys.stdout)
