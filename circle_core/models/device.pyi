# -*- coding: utf-8 -*-

from typing import Dict


class Device(object):
    def __init__(self, schema: str, display_name: str, **kwargs: Dict[str, str]) -> None: ...
    def __str__(self) -> str: ...
