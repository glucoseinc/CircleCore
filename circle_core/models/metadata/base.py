# -*- coding: utf-8 -*-

# system module
from abc import ABCMeta, abstractmethod, abstractproperty
from uuid import UUID

# community module
from six import add_metaclass, PY3

# project module
from circle_core import abstractclassmethod
from ..module import Module
from ..schema import Schema

if PY3:
    from typing import List, Optional


class MetadataError(Exception):
    pass


@add_metaclass(ABCMeta)
class MetadataBase(object):
    """Metadataオブジェクト.

    :param str stringified_type: Metadataタイプ(str)
    """

    stringified_type = 'nothing'

    def __init__(self):
        """init.

        """
        pass

    @abstractclassmethod
    def parse_url_scheme(cls, url_scheme):
        """URLスキームからMetadataオブジェクトを生成する.

        :param str url_scheme: URLスキーム
        :return: Metadataオブジェクト
        :rtype: MetadataBase
        """
        raise NotImplementedError

    @property
    def readable(self):
        """Metadataが読み込み可能か.

        :return: Metadataが読み込み可能か
        :rtype: bool
        """
        return False

    @property
    def writable(self):
        """Metadataが書き込み可能か.

        :return: Metadataが書き込み可能か
        :rtype: bool
        """
        return False


@add_metaclass(ABCMeta)
class MetadataReader(MetadataBase):

    @property
    def readable(self):
        return True

    @abstractproperty
    def schemas(self):
        """全てのSchemaオブジェクト.

        :return: Schemaオブジェクトリスト
        :rtype: List[Schema]
        """
        raise NotImplementedError

    @abstractproperty
    def modules(self):
        """全てのModuleオブジェクト.

        :return: Moduleオブジェクトリスト
        :rtype: List[Module]
        """
        raise NotImplementedError

    def find_schema(self, schema_uuid):
        """スキーマリストからUUIDがマッチするものを取得する.

        :param str schema_uuid: 取得するスキーマのUUID
        :return: マッチしたスキーマ
        :rtype: Optional[Schema]
        """
        if not isinstance(schema_uuid, UUID):
            schema_uuid = UUID(schema_uuid)

        for schema in self.schemas:
            if schema.uuid == schema_uuid:
                return schema
        return None

    def find_module(self, module_uuid):
        """モジュールリストから表示名がマッチするものを取得する.

        :param str module_uuid: 取得するモジュールのUUID
        :return: マッチしたスキーマ
        :rtype: Optional[Module]
        """
        if not isinstance(module_uuid, UUID):
            module_uuid = UUID(module_uuid)

        for module in self.modules:
            if module.uuid == module_uuid:
                return module
        return None


@add_metaclass(ABCMeta)
class MetadataWriter(MetadataBase):
    @property
    def writable(self):
        return True

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
    def register_module(self, module):
        """Moduleオブジェクトをストレージに登録する.

        :param Module module: Moduleオブジェクト
        """
        raise NotImplementedError

    @abstractmethod
    def unregister_module(self, module):
        """Moduleオブジェクトをストレージから削除する.

        :param Module module: Moduleオブジェクト
        """
        raise NotImplementedError

    @abstractmethod
    def update_module(self, module):
        """ストレージ上のModuleオブジェクトを更新する.

        :param Module module: Moduleオブジェクト
        """
        raise NotImplementedError
