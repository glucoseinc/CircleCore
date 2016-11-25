# -*- coding: utf-8 -*-

"""CLI Contextオブジェクト."""

# project module
from ..models import Config, ConfigError


class ContextObjectError(Exception):
    pass


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
        try:
            self.config = Config.parse(config_url)
        except ConfigError as e:
            raise ContextObjectError('Invalid config url / {} : {}'.format(e, config_url))
        self.uuid = crcr_uuid
