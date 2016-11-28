# -*- coding: utf-8 -*-

# system module
from abc import ABCMeta, abstractmethod, abstractproperty

# community module
from six import PY3

# project module
from ..device import Device
from ..schema import Schema

if PY3:
    from typing import List, Optional


class ConfigError(Exception):
    pass


class Config(object):
    """Configオブジェクト.

    :param str stringified_type: Configタイプ(str)
    """

    __metaclass__ = ABCMeta
    stringified_type = 'nothing'

    def __init__(self):
        """init.

        """
        pass

    def matched_schema(self, schema_uuid):
        """スキーマリストからUUIDがマッチするものを取得する.

        :param str schema_uuid: 取得するスキーマのUUID
        :return: マッチしたスキーマ
        :rtype: Optional[Schema]
        """
        for schema in self.schemas:
            if schema.uuid == schema_uuid:
                return schema
        return None

    def matched_device(self, device_uuid):
        """デバイスリストから表示名がマッチするものを取得する.

        :param str device_uuid: 取得するデバイスのUUID
        :return: マッチしたスキーマ
        :rtype: Optional[Device]
        """
        for device in self.devices:
            if device.uuid == device_uuid:
                return device
        return None

    @abstractproperty
    def readable(self):
        """Configが読み込み可能か.

        :return: Configが読み込み可能か
        :rtype: bool
        """
        raise NotImplementedError

    @abstractproperty
    def writable(self):
        """Configが書き込み可能か.

        :return: Configが書き込み可能か
        :rtype: bool
        """
        raise NotImplementedError

    @abstractproperty
    def schemas(self):
        """全てのSchemaオブジェクト.

        :return: Schemaオブジェクトリスト
        :rtype: List[Schema]
        """
        raise NotImplementedError

    @abstractproperty
    def devices(self):
        """全てのDeviceオブジェクト.

        :return: Deviceオブジェクトリスト
        :rtype: List[Device]
        """
        raise NotImplementedError

    @abstractmethod
    def register_schema(self, schema):
        """Schemaオブジェクトをストレージに登録する.

        :param Schema schema: Schemaオブジェクト
        """
        raise NotImplementedError

    @abstractmethod
    def unregister_schema(self, schema):
        """Schemaオブジェクトをストレージから削除する.

        :param Schema schema: Schemaオブジェクト
        """
        raise NotImplementedError

    @abstractmethod
    def register_device(self, device):
        """Deviceオブジェクトをストレージに登録する.

        :param Device device: Deviceオブジェクト
        """
        raise NotImplementedError

    @abstractmethod
    def unregister_device(self, device):
        """Deviceオブジェクトをストレージから削除する.

        :param Device device: Deviceオブジェクト
        """
        raise NotImplementedError

    @abstractmethod
    def update_device(self, device):
        """ストレージ上のDeviceオブジェクトを更新する.

        :param Device device: Deviceオブジェクト
        """
        raise NotImplementedError
