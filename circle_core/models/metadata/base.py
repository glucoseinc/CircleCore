# -*- coding: utf-8 -*-

# system module
from abc import ABCMeta, abstractmethod, abstractproperty
from uuid import UUID

# community module
from six import add_metaclass, PY3

# project module
from circle_core import abstractclassmethod
from ..invitation import Invitation
from ..message_box import MessageBox
from ..module import Module
from ..replication_link import ReplicationLink
from ..schema import Schema
from ..user import User

if PY3:
    from typing import Dict, List, Optional, Union


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
    def parse_url_scheme(cls, url_scheme):  # noqa
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
    def invitations(self):
        """全てのInvitationオブジェクト.

        :return: Invitationオブジェクトリスト
        :rtype: List[Invitation]
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
    def message_boxes(self):
        """全てのMessageBoxオブジェクト.

        :return: MessageBoxオブジェクトリスト
        :rtype: List[MessageBox]
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

    @abstractproperty
    def replication_links(self):
        """全てのReplicationLinkオブジェクト.

        :return: ReplicationLinkオブジェクトリスト
        :rtype: List[ReplicationLink]
        """
        raise NotImplementedError

    def find_invitation(self, uuid):
        """InvitationリストからUUIDがマッチするものを取得する.

        :param Union[str, UUID] uuid: 取得するInvitationのUUID
        :return: マッチしたSchema
        :rtype: Optional[Schema]
        """
        if not isinstance(uuid, UUID):
            try:
                uuid = UUID(uuid)
            except ValueError:
                return None

        for invitation in self.invitations:
            if invitation.uuid == uuid:
                return invitation
        return None

    def find_schema(self, schema_uuid):
        """SchemaリストからUUIDがマッチするものを取得する.

        :param Union[str, UUID] schema_uuid: 取得するSchemaのUUID
        :return: マッチしたSchema
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

    def find_message_box(self, message_box_uuid):
        """MessageBoxリストからUUIDがマッチするものを取得する.

        :param Union[str, UUID] message_box_uuid: 取得するMessageBoxのUUID
        :return: マッチしたMessageBox
        :rtype: Optional[MessageBox]
        """
        if not isinstance(message_box_uuid, UUID):
            try:
                message_box_uuid = UUID(message_box_uuid)
            except ValueError:
                return None

        for message_box in self.message_boxes:
            if message_box.uuid == message_box_uuid:
                return message_box
        return None

    def find_message_boxes_by_schema(self, schema_uuid):
        """MessageBoxリストからschema_uuidがマッチするものを取得する.

        :param Union[str, UUID] schema_uuid: 取得するSchemaのUUID
        :return: マッチしたMessageBoxのリスト
        :rtype: List[MessageBox]
        """
        if not isinstance(schema_uuid, UUID):
            try:
                schema_uuid = UUID(schema_uuid)
            except ValueError:
                return []

        return [message_box for message_box in self.message_boxes if message_box.schema_uuid == schema_uuid]

    def find_module(self, module_uuid):
        """ModuleリストからUUIDがマッチするものを取得する.

        :param Union[str, UUID] module_uuid: 取得するModuleのUUID
        :return: マッチしたModule
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

    def find_modules_by_schema(self, schema_uuid):
        """Moduleリストからschema_uuidがマッチするものを取得する.

        :param Union[str, UUID] schema_uuid: 取得するSchemaのUUID
        :return: マッチしたModuleのリスト
        :rtype: List[Module]
        """
        message_boxes = self.find_message_boxes_by_schema(schema_uuid)
        message_box_uuids = set([message_box.uuid for message_box in message_boxes])
        modules = []
        for module in self.modules:  # type: Module
            if len(set(module.message_box_uuids).intersection(message_box_uuids)) > 0:
                modules.append(module)
        return modules

    def find_replication_link(self, replication_link_uuid):
        """ReplicationLinkリストからUUIDがマッチするものを取得する.

        :param Union[str, UUID] replication_link_uuid: 取得するReplicationLinkのUUID
        :return: マッチしたReplicationLink
        :rtype: Optional[ReplicationLink]
        """
        if not isinstance(replication_link_uuid, UUID):
            try:
                replication_link_uuid = UUID(replication_link_uuid)
            except ValueError:
                return None

        for module in self.replication_links:
            if module.uuid == replication_link_uuid:
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

    def denormalize_json_message_box(self, message_box_uuid):
        """MessageBoxに情報を付与したJSON表現を返す.

        :param Union[str, UUID] message_box_uuid: 取得するMessageBoxのUUID
        :return: json表現のdict
        :rtype: Dict
        """
        message_box = self.find_message_box(message_box_uuid)
        if message_box is None:
            return {}
        dic = message_box.to_json()
        schema = self.find_schema(message_box.schema_uuid)
        dic['schema'] = schema.to_json() if schema is not None else {}
        dic.pop('schema_uuid', None)
        return dic

    def denormalize_json_module(self, module_uuid):
        """ModuleにMessageBox情報を付与したJSON表現を返す.

        :param Union[str, UUID] module_uuid: 取得するModuleのUUID
        :return: json表現のdict
        :rtype: Dict
        """
        module = self.find_module(module_uuid)
        if module is None:
            return {}
        dic = module.to_json()
        dic['message_boxes'] = [self.denormalize_json_message_box(message_box_uuid)
                                for message_box_uuid in module.message_box_uuids]
        dic.pop('message_box_uuids', None)
        return dic

    def json_schema_with_module(self, schema_uuid):
        """SchemaにModule情報を付与したJSON表現を返す.

        :param Union[str, UUID] schema_uuid: 取得するSchemaのUUID
        :return: json表現のdict
        :rtype: Dict
        """
        schema = self.find_schema(schema_uuid)
        if schema is None:
            return {}
        dic = schema.to_json()
        modules = self.find_modules_by_schema(schema_uuid)
        dic['modules'] = [module.to_json() for module in modules]
        return dic


@add_metaclass(ABCMeta)
class MetadataWriter(MetadataBase):
    @property
    def writable(self):
        return True

    # Invitation
    @abstractmethod
    def register_invitation(self, invitation):
        """Invitationオブジェクトをストレージに登録する.

        :param Invitation invitation: Invitationオブジェクト
        :return: 成功/失敗
        :rtype: bool
        """
        raise NotImplementedError

    @abstractmethod
    def unregister_invitation(self, invitation):
        """Invitationオブジェクトをストレージから削除する.

        :param Invitation invitation: Invitationオブジェクト
        :return: 成功/失敗
        :rtype: bool
        """
        raise NotImplementedError

    @abstractmethod
    def update_invitation(self, invitation):
        """ストレージ上のInvitationオブジェクトを更新する.

        :param Invitation invitation: Invitationオブジェクト
        :return: 成功/失敗
        :rtype: bool
        """

    # Schema
    @abstractmethod
    def register_schema(self, schema):
        """Schemaオブジェクトをストレージに登録する.

        :param Schema schema: Schemaオブジェクト
        :return: 成功/失敗
        :rtype: bool
        """
        raise NotImplementedError

    @abstractmethod
    def unregister_schema(self, schema):
        """Schemaオブジェクトをストレージから削除する.

        :param Schema schema: Schemaオブジェクト
        :return: 成功/失敗
        :rtype: bool
        """
        raise NotImplementedError

    @abstractmethod
    def update_schema(self, schema):
        """ストレージ上のSchemaオブジェクトを更新する.

        :param Schema schema: Schemaオブジェクト
        :return: 成功/失敗
        :rtype: bool
        """
        raise NotImplementedError

    @abstractmethod
    def register_message_box(self, message_box):
        """MessageBoxオブジェクトをストレージに登録する.

        :param MessageBox message_box: MessageBoxオブジェクト
        :return: 成功/失敗
        :rtype: bool
        """
        raise NotImplementedError

    @abstractmethod
    def unregister_message_box(self, message_box):
        """MessageBoxオブジェクトをストレージから削除する.

        :param MessageBox message_box: MessageBoxオブジェクト
        :return: 成功/失敗
        :rtype: bool
        """
        raise NotImplementedError

    @abstractmethod
    def update_message_box(self, message_box):
        """ストレージ上のMessageBoxオブジェクトを更新する.

        :param MessageBox message_box: MessageBoxオブジェクト
        :return: 成功/失敗
        :rtype: bool
        """
        raise NotImplementedError

    @abstractmethod
    def register_module(self, module):
        """Moduleオブジェクトをストレージに登録する.

        :param Module module: Moduleオブジェクト
        :return: 成功/失敗
        :rtype: bool
        """
        raise NotImplementedError

    @abstractmethod
    def unregister_module(self, module):
        """Moduleオブジェクトをストレージから削除する.

        :param Module module: Moduleオブジェクト
        :return: 成功/失敗
        :rtype: bool
        """
        raise NotImplementedError

    @abstractmethod
    def update_module(self, module):
        """ストレージ上のModuleオブジェクトを更新する.

        :param Module module: Moduleオブジェクト
        :return: 成功/失敗
        :rtype: bool
        """
        raise NotImplementedError

    @abstractmethod
    def register_user(self, user):
        """Userオブジェクトをストレージに登録する.

        :param User user: Userオブジェクト
        :return: 成功/失敗
        :rtype: bool
        """
        raise NotImplementedError

    @abstractmethod
    def unregister_user(self, user):
        """Userオブジェクトをストレージから削除する.

        :param User user: Userオブジェクト
        :return: 成功/失敗
        :rtype: bool
        """
        raise NotImplementedError

    @abstractmethod
    def update_user_last_access(self, user_id, datetime):
        """Userの最終アクセス時刻を記録する

        :param UUID user_id: UserのID
        :param datetime datetime.datetime: 最終アクセス時刻(UTC)
        :return: 成功/失敗
        :rtype: bool
        """
        raise NotImplementedError

    @abstractmethod
    def get_user_last_access(self, user_id):
        """Userの最終アクセス時刻を記録する

        :param UUID user_id: UserのID
        :return: 成功/失敗
        :rtype: datetime.datetime
        """
        raise NotImplementedError
