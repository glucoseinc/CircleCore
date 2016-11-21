from sys import stdout
from logging import getLogger, DEBUG, StreamHandler


logger = getLogger('circle_core')
logger.setLevel(DEBUG)
stream = StreamHandler(stdout)
stream.setLevel(DEBUG)
logger.addHandler(stream)
