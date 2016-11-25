#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from circle_core.models.config import Config

from tests import test_root


class TestConfig(object):
    def test_init(self):
        config = Config(schemas=[], devices=[])
        assert config.schemas == []
        assert config.devices == []

    def test_parse(self):
        url_string = 'file://{}'.format(os.path.join(test_root, 'config.ini'))
        config = Config.parse(url_string)
        assert len(config.schemas) == 1
        assert len(config.devices) == 1
