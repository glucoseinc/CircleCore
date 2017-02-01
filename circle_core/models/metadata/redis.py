# -*- coding: utf-8 -*-

# system module
from __future__ import absolute_import

import datetime
import uuid

# community module
from redis import ConnectionError, Redis
from six import PY3

# project module
# TODO: cli.utilsから外に移す
from circle_core.utils import format_date, prepare_date
from .base import MetadataError, MetadataReader, MetadataWriter
from ..cc_info import CcInfo
from ..invitation import Invitation
from ..message_box import MessageBox
from ..module import Module
from ..replication_link import ReplicationLink
from ..schema import Schema
from ..user import User

if PY3:
    from typing import Any, Dict, List, Optional, Union


class RedisClient(Redis):
    """Redisクライアント."""

    def parse_response(self, connection, command_name, **options):
        """Parses a response from the Redis server."""
        def decoded(word):
            """bytesはstrに変換する."""
            return word.decode('utf-8') if isinstance(word, bytes) else word

        response = super(RedisClient, self).parse_response(connection, command_name, **options)

        if PY3:
            if isinstance(response, bytes):
                return decoded(response)
            elif isinstance(response, list):
                return [decoded(resp) for resp in response]
            elif isinstance(response, dict):
                return {decoded(k): decoded(v) for k, v in response.items()}
        return response


class MetadataRedis(MetadataReader, MetadataWriter):
    """MetadataRedisオブジェクト.

    :param RedisClient redis_client: Redisクライアント
    """

    stringified_type = 'Redis'

    def __init__(self, redis_client):
        """init.

        :param RedisClient redis_client: Redisクライアント
        """
        super(MetadataRedis, self).__init__()
        self.redis_client = redis_client

    @classmethod
    def parse_url_scheme(cls, url_scheme):
        """URLスキームからMetadataオブジェクトを生成する.

        :param str url_scheme: URLスキーム
        :return: Metadataオブジェクト
        :rtype: MetadataRedis
        """
        try:
            redis_client = RedisClient.from_url(url_scheme)
            redis_client.ping()
        except ConnectionError:
            raise MetadataError('Cannot connect to Redis server.')

        return MetadataRedis(redis_client)

    @property
    def invitations(self):
        """全てのInvitationオブジェクト.

        :return: Schemaオブジェクトリスト
        :rtype: List[Schema]
        """
        invitations = []
        for key in self.redis_client.keys():
            if not Invitation.is_key_matched(key):
                continue

            if self.redis_client.type(key) == 'hash':
                d = self.redis_client.hgetall(key)  # type: Dict[str, Any]
                invitations.append(Invitation.from_json(d))
        return invitations

    @property
    def schemas(self):
        """全てのSchemaオブジェクト.

        :return: Schemaオブジェクトリスト
        :rtype: List[Schema]
        """
        schemas = []
        keys = [key for key in self.redis_client.keys() if Schema.is_key_matched(key)]
        for key in keys:
            if self.redis_client.type(key) == 'hash':
                fields = self.redis_client.hgetall(key)  # type: Dict[str, Any]
                properties_string = fields.pop('properties', None)  # type: Optional[str]
                if properties_string is not None:
                    fields['dictified_properties'] = Schema.dictify_properties(properties_string)
                schemas.append(Schema(**fields))
        return schemas

    @property
    def message_boxes(self):
        """全てのMessageBoxオブジェクト.

        :return: MessageBoxオブジェクトリスト
        :rtype: List[MessageBox]
        """
        message_boxes = []
        keys = [key for key in self.redis_client.keys() if MessageBox.is_key_matched(key)]
        for key in keys:
            if self.redis_client.type(key) == 'hash':
                fields = self.redis_client.hgetall(key)  # type: Dict[str, Any]
                message_boxes.append(MessageBox(**fields))
        return message_boxes

    @property
    def modules(self):
        """全てのModuleオブジェクト.

        :return: Moduleオブジェクトリスト
        :rtype: List[Module]
        """
        modules = []
        keys = [key for key in self.redis_client.keys() if Module.is_key_matched(key)]
        for key in keys:
            if self.redis_client.type(key) == 'hash':
                fields = self.redis_client.hgetall(key)  # type: Dict[str, Any]
                message_box_uuids = fields.pop('message_box_uuids', None)  # type: Union[str, None]
                if message_box_uuids is not None:
                    fields['message_box_uuids'] = message_box_uuids.split(',')
                modules.append(Module(**fields))
        return modules

    @property
    def users(self):
        """全てのUserオブジェクト.

        :return: Userオブジェクトリスト
        :rtype: List[User]
        """
        users = []
        keys = [key for key in self.redis_client.keys() if User.is_key_matched(key)]
        for key in keys:
            if self.redis_client.type(key) == 'hash':
                fields = self.redis_client.hgetall(key)  # type: Dict[str, Any]
                obj = User.from_json(fields)

                # 最終アクセス時刻
                obj.date_last_access = self.get_user_last_access(obj.uuid)

                users.append(obj)
        return users

    @property
    def replication_links(self):
        """全てのReplicationLinkオブジェクト.

        :return: ReplicationLinkオブジェクトリスト
        :rtype: List[ReplicationLink]
        """
        replication_links = []
        keys = [key for key in self.redis_client.keys() if ReplicationLink.is_key_matched(key)]
        for key in keys:
            if self.redis_client.type(key) == 'hash':
                fields = self.redis_client.hgetall(key)  # type: Dict[str, Any]
                replication_links.append(ReplicationLink(**fields))
        return replication_links

    @property
    def cc_infos(self):
        """全てのCircleCoreInfoオブジェクト.

        :return: CircleCoreInfoオブジェクトリスト
        :rtype: List[CcInfo]
        """
        cc_infos = []
        keys = [key for key in self.redis_client.keys() if CcInfo.is_key_matched(key)]
        for key in keys:
            if self.redis_client.type(key) == 'hash':
                fields = self.redis_client.hgetall(key)  # type: Dict[str, Any]
                cc_infos.append(CcInfo(**fields))
        return cc_infos

    # Invitation
    def register_invitation(self, obj):
        """Invitationオブジェクトをストレージに登録する.

        :param Invitation obj: Invitationオブジェクト
        :return: 成功/失敗
        :rtype: bool
        """
        if not obj.uuid:
            obj.uuid = self._generate_uuid(Invitation)
        self.redis_client.hmset(obj.storage_key, obj.to_json())
        return True

    def unregister_invitation(self, invitation):
        """Invitationオブジェクトをストレージから削除する.

        :param Invitation invitation: Invitationオブジェクト
        :return: 成功/失敗
        :rtype: bool
        """
        return True if self.redis_client.delete(invitation.storage_key) > 0 else False

    def update_invitation(self, invitation):
        """ストレージ上のInvitationオブジェクトを更新する.

        :param Invitation invitation: Invitationオブジェクト
        :return: 成功/失敗
        :rtype: bool
        """
        if self.unregister_invitation(invitation) is True:
            return self.register_invitation(invitation)
        return False

    # Schema
    def register_schema(self, schema):
        """Schemaオブジェクトをストレージに登録する.

        :param Schema schema: Schemaオブジェクト
        :return: 成功/失敗
        :rtype: bool
        """
        mapping = {
            'uuid': schema.uuid,
            'display_name': schema.display_name,
            'properties': schema.stringified_properties,
        }
        if schema.memo is not None:
            mapping['memo'] = schema.memo

        self.redis_client.hmset(schema.storage_key, mapping)
        return True

    def unregister_schema(self, schema):
        """Schemaオブジェクトをストレージから削除する.

        :param Schema schema: Schemaオブジェクト
        :return: 成功/失敗
        :rtype: bool
        """
        if len(self.find_modules_by_schema(schema.uuid)) != 0:
            return False

        self.redis_client.delete(schema.storage_key)
        return True

    def update_schema(self, schema):
        """ストレージ上のSchemaオブジェクトを更新する.

        :param Schema schema: Schemaオブジェクト
        :return: 成功/失敗
        :rtype: bool
        """
        if self.unregister_schema(schema) is True:
            return self.register_schema(schema)
        return False

    # MessageBox
    def register_message_box(self, message_box):
        """MessageBoxオブジェクトをストレージに登録する.

        :param MessageBox message_box: MessageBoxオブジェクト
        :return: 成功/失敗
        :rtype: bool
        """
        mapping = {
            'uuid': message_box.uuid,
            'schema_uuid': message_box.schema_uuid,
            'display_name': message_box.display_name,
            'master_uuid': message_box.master_uuid or ''
        }
        if message_box.memo is not None:
            mapping['memo'] = message_box.memo

        self.redis_client.hmset(message_box.storage_key, mapping)
        return True

    def unregister_message_box(self, message_box):
        """MessageBoxオブジェクトをストレージから削除する.

        :param MessageBox message_box: MessageBoxオブジェクト
        :return: 成功/失敗
        :rtype: bool
        """
        self.redis_client.delete(message_box.storage_key)
        return True

    def update_message_box(self, message_box):
        """ストレージ上のMessageBoxオブジェクトを更新する.

        :param MessageBox message_box: MessageBoxオブジェクト
        :return: 成功/失敗
        :rtype: bool
        """
        if self.unregister_message_box(message_box) is True:
            return self.register_message_box(message_box)
        return False

    # Module
    def register_module(self, module):
        """Moduleオブジェクトをストレージに登録する.

        :param Module module: Moduleオブジェクト
        :return: 成功/失敗
        :rtype: bool
        """
        mapping = {
            'uuid': module.uuid,
            'message_box_uuids': module.stringified_message_box_uuids,
            'display_name': module.display_name,
            'tags': module.stringified_tags,
        }
        if module.memo is not None:
            mapping['memo'] = module.memo

        self.redis_client.hmset(module.storage_key, mapping)
        return True

    def unregister_module(self, module):
        """Moduleオブジェクトをストレージから削除する.

        :param Module module: Moduleオブジェクト
        :return: 成功/失敗
        :rtype: bool
        """
        # TODO: Module削除時には紐づいているMessageBoxも一緒に削除する
        self.redis_client.delete(module.storage_key)
        return True

    def update_module(self, module):
        """ストレージ上のModuleオブジェクトを更新する.

        :param Module module: Moduleオブジェクト
        :return: 成功/失敗
        :rtype: bool
        """
        if self.unregister_module(module) is True:
            return self.register_module(module)
        return False

    # User
    def register_user(self, new_user):
        """Userオブジェクトをストレージに登録する.

        :param User new_user: Userオブジェクト
        :return: 成功/失敗
        :rtype: bool
        """
        # TODO: transactionを使う
        for user in self.users:
            if user.account == new_user.account:
                raise ValueError('account is already used')
        d = new_user.to_json(True)
        d['permissions'] = ','.join(d['permissions'])
        self.redis_client.hmset(new_user.storage_key, d)
        return True

    def unregister_user(self, user):
        """Userオブジェクトをストレージから削除する.

        :param User user: Userオブジェクト
        :return: 成功/失敗
        :rtype: bool
        """
        self.redis_client.delete(user.storage_key)
        return True

    def update_user_last_access(self, user_id, dt):
        """Userの最終アクセス時刻を記録する.

        :param UUID user_id: UserのID
        :param datetime.datetime dt: 最終アクセス時刻(UTC)
        :return: 成功/失敗
        :rtype: bool
        """
        assert isinstance(dt, datetime.datetime)

        dt = prepare_date(dt)
        self.redis_client.set(User.make_key_for_last_access(user_id), format_date(dt))
        print('update date', user_id, dt)

    def get_user_last_access(self, user_id):
        """Userの最終アクセス時刻を記録する.

        :param UUID user_id: UserのID
        :return: 成功/失敗
        :rtype: datetime.datetime
        """
        val = self.redis_client.get(User.make_key_for_last_access(user_id))
        if not val:
            return None
        return prepare_date(val)

    # CcInfo
    def register_cc_info(self, cc_info):
        """CircleCoreInfoオブジェクトをストレージに登録する.

        :param CcInfo cc_info: CircleCoreInfoオブジェクト
        :return: 成功/失敗
        :rtype: bool
        """
        mapping = {
            'uuid': cc_info.uuid,
            'display_name': cc_info.display_name,
            'myself': cc_info.myself,
        }
        if cc_info.work is not None:
            mapping['work'] = cc_info.work

        self.redis_client.hmset(cc_info.storage_key, mapping)
        # TODO: 登録時に myself is True が2個以上存在しないようにする必要がある
        return True

    def unregister_cc_info(self, cc_info):
        """CircleCoreInfoオブジェクトをストレージから削除する.

        :param CcInfo cc_info: CircleCoreInfoオブジェクト
        :return: 成功/失敗
        :rtype: bool
        """
        if len(self.find_modules_by_schema(cc_info.uuid)) != 0:
            return False

        self.redis_client.delete(cc_info.storage_key)
        return True

    def update_cc_info(self, cc_info):
        """ストレージ上のCircleCoreInfoオブジェクトを更新する.

        :param CcInfo cc_info: CircleCoreInfoオブジェクト
        :return: 成功/失敗
        :rtype: bool
        """
        if self.register_cc_info(cc_info) is True:
            return self.unregister_cc_info(cc_info)
        return False

    # Private methods
    def _generate_uuid(self, model_class):
        while True:
            generated = uuid.uuid4()
            if not self.redis_client.exists(model_class.make_storage_key(generated)):
                break
        return generated
