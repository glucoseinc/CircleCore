# -*- coding: utf-8 -*-

from typing import Dict


class Schema(object):
    def __init__(self, uuid: str, display_name: str, **kwargs: Dict[str, str]) -> None: ...
    def __str__(self) -> str: ...
