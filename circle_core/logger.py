# -*- coding: utf-8 -*-
"""Logger."""

# system module
import logging
import os

try:
    import colorama

    class NiceColoredFormatter(logging.Formatter):
        """色がでるFormatter!!!"""

        short_levelname_map = {'DEBUG': 'DBUG', 'INFO': 'INFO', 'WARNING': 'WARN', 'ERROR': 'ERRO', 'CRITICAL': 'CRIT'}
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
            return '{}{}{}'.format(color, text, colorama.Style.RESET_ALL)

        def formatMessage(self, record):  # noqa
            if isinstance(record, logging.LogRecord):
                record.nice_levelname = self._colored(
                    self.level_color_map[record.levelname], '[{}]'.format(self.short_levelname_map[record.levelname])
                )

                record.nice_name = self._colored(self.name_color, record.name)
                if hasattr(record, 'asctime'):
                    record.asctime = self._colored(self.asctime_color, record.asctime)

            return self._style.format(record) + colorama.Style.RESET_ALL
except ImportError:
    pass

logger = logging.getLogger('circle_core')
