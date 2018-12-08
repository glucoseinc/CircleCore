# -*- coding: utf-8 -*-
"""CLI Contextオブジェクト."""


class CLIContextObject(object):
    """CLI Contextオブジェクト.

    :param CircleCore core: CircleCore
    """

    def __init__(self, core):
        """init.

        :param CircleCore core: CircleCore
        """
        self.core = core
