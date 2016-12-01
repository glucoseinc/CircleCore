# -*- coding: utf-8 -*-

"""CircleCore."""

# system module
from logging import basicConfig, DEBUG
import sys


basicConfig(format='%(levelname)s:%(name)s - %(message)s', level=DEBUG, stream=sys.stdout)
