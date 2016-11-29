# -*- coding: utf-8 -*-
import os

import pytest

from circle_core.models.config import Config, ConfigError, ConfigIniFile, ConfigRedis, parse_url_scheme
from tests import ini_file_path, url_scheme_ini_file


class TestConfig(object):
    def test_init(self):
        with pytest.raises(TypeError):
            Config()

    def test_parse(self):
        with pytest.raises(ConfigError):
            parse_url_scheme('mysql://user:password@server:3306/circle_core')

        assert isinstance(parse_url_scheme(url_scheme_ini_file), ConfigIniFile)
        url_scheme_redis = os.environ['CRCR_CONFIG']
        assert isinstance(parse_url_scheme(url_scheme_redis), ConfigRedis)


class TestConfigIniFile(object):
    def test_property(self):
        config = ConfigIniFile(ini_file_path)
        assert config.readable is True
        assert config.writable is False
