# -*- coding: utf-8 -*-

from typing import List
from ..models import Config, Schema, Device


class Config(object):

    def __init__(self, schemas: List[Schema], devices: List[Device]) -> None: ...
    def __str__(self) -> str: ...
    @classmethod
    def parse(cls, url_string: str) -> Config: ...
