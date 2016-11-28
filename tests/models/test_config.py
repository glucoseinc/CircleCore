# -*- coding: utf-8 -*-

from circle_core.models.config import ConfigError, ConfigIniFile, parse_url_scheme
import pytest

from tests import ini_file_path, url_scheme_ini_file


class TestConfig(object):
    def test_init(self):
        config = ConfigIniFile(ini_file_path)
        assert len(config.schemas) == 2
        assert len(config.devices) == 1

    def test_parse(self):
        config = parse_url_scheme(url_scheme_ini_file)
        assert len(config.schemas) == 2
        assert len(config.devices) == 1

        with pytest.raises(ConfigError):
            parse_url_scheme('mysql://user:password@server:3306/circle_core')
