# -*- coding: utf-8 -*-
import os

import pytest

from circle_core.models.metadata import Metadata, MetadataError, MetadataIniFile, MetadataRedis, parse_url_scheme
from tests import ini_file_path, url_scheme_ini_file


class TestMetadata(object):
    def test_init(self):
        with pytest.raises(TypeError):
            Metadata()

    def test_parse(self):
        with pytest.raises(MetadataError):
            parse_url_scheme('mysql://user:password@server:3306/circle_core')

        assert isinstance(parse_url_scheme(url_scheme_ini_file), MetadataIniFile)
        url_scheme_redis = os.environ['CRCR_METADATA']
        assert isinstance(parse_url_scheme(url_scheme_redis), MetadataRedis)


class TestMetadataIniFile(object):
    def test_property(self):
        metadata = MetadataIniFile(ini_file_path)
        assert metadata.readable is True
        assert metadata.writable is False
