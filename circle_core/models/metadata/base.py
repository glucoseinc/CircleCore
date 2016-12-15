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
from ..user import User

if PY3:
    from typing import List, Optional, Union


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
        """Metadataが読み込み可能か.

        :return: Metadataが読み込み可能か
        :rtype: bool
        """
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

    @abstractproperty
    def users(self):
        """全てのUserオブジェクト.

        :return: Userオブジェクトリスト
        :rtype: List[User]
        """
        raise NotImplementedError

    def find_schema(self, schema_uuid):
        """スキーマリストからUUIDがマッチするものを取得する.

        :param Union[str, UUID] schema_uuid: 取得するスキーマのUUID
        :return: マッチしたスキーマ
        :rtype: Optional[Schema]
        """
        if not isinstance(schema_uuid, UUID):
            try:
                schema_uuid = UUID(schema_uuid)
            except ValueError:
                return None

        for schema in self.schemas:
            if schema.uuid == schema_uuid:
                return schema
        return None

    def find_module(self, module_uuid):
        """モジュールリストからUUIDがマッチするものを取得する.

        :param Union[str, UUID] module_uuid: 取得するモジュールのUUID
        :return: マッチしたモジュール
        :rtype: Optional[Module]
        """
        if not isinstance(module_uuid, UUID):
            try:
                module_uuid = UUID(module_uuid)
            except ValueError:
                return None

        for module in self.modules:
            if module.uuid == module_uuid:
                return module
        return None

    def find_user(self, user_uuid):
        """ユーザリストからUUIDがマッチするものを取得する.

        :param Union[str, UUID] user_uuid: 取得するユーザのUUID
        :return: マッチしたユーザ
        :rtype: Optional[User]
        """
        if not isinstance(user_uuid, UUID):
            try:
                user_uuid = UUID(user_uuid)
            except ValueError:
                return None

        for user in self.users:  # type: User
            if user.uuid == user_uuid:
                return user
        return None

    def find_user_by_mail_address(self, mail_address):
        """ユーザリストからメールアドレスがマッチするものを取得する.

        :param str mail_address: 取得するユーザのメールアドレス
        :return: マッチしたユーザ
        :rtype: Optional[User]
        """
        for user in self.users:  # type: User
            if user.mail_address == mail_address:
                return user
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

    @abstractmethod
    def register_user(self, user):
        """Userオブジェクトをストレージに登録する.

        :param User user: Userオブジェクト
        """
        raise NotImplementedError

    @abstractmethod
    def unregister_user(self, user):
        """Userオブジェクトをストレージから削除する.

        :param User user: Userオブジェクト
        """
        raise NotImplementedError
