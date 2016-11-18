#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""CLI Contextオブジェクト."""

# project module
from ..models import Config


class ContextObject(object):
    """CLI Contextオブジェクト.

    :param str config_url: ConfigのURLスキーム
    :param Config config: Configオブジェクト
    :param str uuid: CircleCore UUID
    """

    def __init__(self, config_url, crcr_uuid):
        """init.

        :param str config_url: ConfigのURLスキーム
        :param str crcr_uuid: CircleCore UUID
        """
        self.config_url = config_url
        self.config = Config.parse(config_url)
        self.uuid = crcr_uuid
