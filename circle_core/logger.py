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


try:
    import colorama

    class NiceColoredFormatter(logging.Formatter):
        """色がでるFormatter!!!"""

        short_levelname_map = {
            'DEBUG': 'DBUG',
            'INFO': 'INFO',
            'WARNING': 'WARN',
            'ERROR': 'ERRO',
            'CRITICAL': 'CRIT'
        }
        level_color_map = {
            'DEBUG': colorama.Style.DIM + colorama.Fore.WHITE,
            'INFO': colorama.Fore.WHITE,
            'WARNING': colorama.Fore.YELLOW,
            'ERROR': colorama.Fore.RED,
            'CRITICAL': colorama.Style.BRIGHT + colorama.Fore.RED + colorama.Back.WHITE,
        }
        name_color = colorama.Fore.MAGENTA
        asctime_color = colorama.Style.DIM + colorama.Fore.WHITE

        def _colored(self, color, text):
            return '{}{}{}'.format(
                color, text, colorama.Style.RESET_ALL
            )

        def formatMessage(self, record):  # noqa
            if isinstance(record, logging.LogRecord):
                record.nice_levelname = self._colored(
                    self.level_color_map[record.levelname],
                    '[{}]'.format(self.short_levelname_map[record.levelname])
                )

                record.nice_name = self._colored(self.name_color, record.name)
                if hasattr(record, 'asctime'):
                    record.asctime = self._colored(self.asctime_color, record.asctime)

            return self._style.format(record) + colorama.Style.RESET_ALL
except ImportError:
    pass


def get_stream_logger(name=None):
    logger = logging.getLogger(name)
    return logger
