#!/usr/bin/env python
# -*- coding: utf-8 -*-

from circle_core.models.config import Config, ConfigError
import pytest

from tests import url_scheme_ini_file


class TestConfig(object):
    def test_init(self):
        config = Config(schemas=[], devices=[])
        assert config.schemas == []
        assert config.devices == []

    def test_parse(self):
        config = Config.parse(url_scheme_ini_file)
        assert len(config.schemas) == 2
        assert len(config.devices) == 1

        with pytest.raises(ConfigError):
            Config.parse('mysql://user:password@server:3306/circle_core')
