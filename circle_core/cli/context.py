# -*- coding: utf-8 -*-

"""CLI Contextオブジェクト."""

# community module
from six import PY3

# project module
from circle_core.logger import LTSVLogger
from ..models import Metadata, MetadataError
from ..models.metadata import parse_url_scheme

if PY3:
    from typing import Optional


class ContextObjectError(Exception):
    pass


class ContextObject(object):
    """CLI Contextオブジェクト.

    :param str metadata_url: MetadataのURLスキーム
    :param Metadata metadata: Metadataオブジェクト
    :param str uuid: CircleCore UUID
    :param Optional[str] log_file_path: ログファイルのパス
    :param LTSVLogger _logger: Logger
    """

    def __init__(self, metadata_url, crcr_uuid, log_file_path):
        """init.

        :param str metadata_url: MetadataのURLスキーム
        :param str crcr_uuid: CircleCore UUID
        :param Optional[str] log_file_path: ログファイルのパス
        """
        self.metadata_url = metadata_url
        try:
            self.metadata = parse_url_scheme(metadata_url)
        except MetadataError as e:
            raise ContextObjectError('Invalid metadata url / {} : {}'.format(e, metadata_url))
        self.uuid = crcr_uuid
        self.log_file_path = log_file_path
        self._logger = LTSVLogger(name='cli_logger', log_file_path=log_file_path)

    def log_info(self, operation, **details):
        """ログをファイルに書き込む.

        :param str operation:
        :param Dict[str, str] details:
        """
        self._logger.info(user_id='0', operation=operation, **details)
