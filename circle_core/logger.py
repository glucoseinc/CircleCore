# -*- coding: utf-8 -*-

"""Logger."""

# system module
import logging
import os


class LTSVLogger(object):
    def __init__(self, name=None, log_file_path=None, level=logging.DEBUG):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        self._set_handler(log_file_path, level)

    def _set_handler(self, log_file_path, level):
        self.logger.handlers = []
        handler = logging.StreamHandler()
        if log_file_path is not None:
            try:
                os.makedirs(os.path.dirname(log_file_path))
            except OSError:
                pass
            handler = logging.FileHandler(log_file_path)

        handler.setLevel(level)
        formatter = logging.Formatter(
            fmt='time:%(asctime)s\t%(message)s',
            datefmt='%Y-%m-%dT%H:%M:%S%z',
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def info(self, user_id, operation, **details):
        _details = ''
        if len(details):
            for key, value in details.items():
                _details += '\t{}:{}'.format(key, value)
        message = 'user_id:{user_id}\toperation:{operation}{details}'.format(user_id=user_id,
                                                                             operation=operation,
                                                                             details=_details)
        self.logger.info(message)


# TODO: temporary
def get_stream_legger(name=None, level=logging.DEBUG):
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(logging.StreamHandler())
    return logger
