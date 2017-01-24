# -*- coding: utf-8 -*-
from os import environ
from uuid import UUID

import pytest

from circle_core.models.message_box import MessageBox
from circle_core.models.metadata import Metadata, MetadataError, MetadataIniFile, MetadataRedis, parse_url_scheme
from circle_core.models.module import Module
from circle_core.models.schema import Schema
from tests import ini_file_name, ini_file_path, url_scheme_ini_file


class TestMetadata(object):
    def test_init(self):
        with pytest.raises(TypeError):
            Metadata()

    def test_parse(self):
        with pytest.raises(MetadataError):
            parse_url_scheme('mysql://user:password@server:3306/circle_core')

        with pytest.raises(MetadataError):
            parse_url_scheme('file://{}'.format(ini_file_name))

        assert isinstance(parse_url_scheme(url_scheme_ini_file), MetadataIniFile)
        url_scheme_redis = environ['CRCR_METADATA']
        assert isinstance(parse_url_scheme(url_scheme_redis), MetadataRedis)


class TestMetadataIniFile(object):
    def test_property(self):
        metadata = MetadataIniFile(ini_file_path)
        assert metadata.readable is True
        assert metadata.writable is False


class TestMetadataRedis(object):
    def test_store_and_restore(self, redis_server):
        """Redisへの保存、そこからのPythonオブジェクトの復元のテスト."""
        metadata = MetadataRedis.parse_url_scheme(environ['CRCR_METADATA'])

        schema = Schema(
            '44ae2fd8-52d0-484d-9a48-128b07937a0a',
            'DummySchema',
            [{'name': 'hoge', 'type': 'int'}],
            'memo'
        )
        metadata.register_schema(schema)
        assert len(metadata.schemas) == 1
        assert metadata.schemas[0].uuid == UUID('44ae2fd8-52d0-484d-9a48-128b07937a0a')
        assert metadata.schemas[0].display_name == 'DummySchema'
        assert metadata.schemas[0].dictified_properties == [{'name': 'hoge', 'type': 'int'}]
        assert metadata.schemas[0].memo == 'memo'

        box = MessageBox(
            '316720eb-84fe-43b3-88b7-9aad49a93220',
            '44ae2fd8-52d0-484d-9a48-128b07937a0a',
            'DummyBox',
            'message box for test',
        )
        metadata.register_message_box(box)
        assert len(metadata.message_boxes) == 1
        assert metadata.message_boxes[0].uuid == UUID('316720eb-84fe-43b3-88b7-9aad49a93220')
        assert metadata.message_boxes[0].schema_uuid == UUID('44ae2fd8-52d0-484d-9a48-128b07937a0a')
        assert metadata.message_boxes[0].display_name == 'DummyBox'
        assert metadata.message_boxes[0].memo == 'message box for test'
        assert not metadata.message_boxes[0].master_uuid

        module = Module(
            '8e654793-5c46-4721-911e-b9d19f0779f9',
            ['316720eb-84fe-43b3-88b7-9aad49a93220'],
            'DummyModule',
            'foo,bar',
            'some description'
        )
        metadata.register_module(module)
        assert len(metadata.modules) == 1
        assert metadata.modules[0].uuid == UUID('8e654793-5c46-4721-911e-b9d19f0779f9')
        assert metadata.modules[0].message_box_uuids == [UUID('316720eb-84fe-43b3-88b7-9aad49a93220')]
        assert metadata.modules[0].display_name == 'DummyModule'
        assert metadata.modules[0].tags == ['foo', 'bar']
        assert metadata.modules[0].memo == 'some description'
