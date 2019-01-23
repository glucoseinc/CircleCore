# -*- coding: utf-8 -*-
"""CLI Contextオブジェクト."""


class CLIContextObject(object):
    """CLI Contextオブジェクト.

    Attributes:
        core (circle_core.core.CircleCore): CircleCore

    Args:
        core (circle_core.core.CircleCore): CircleCore
    """

    def __init__(self, core):
        self.core = core
