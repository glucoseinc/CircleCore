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
from ..invitation import Invitation
from ..message_box import MessageBox
from ..module import Module
from ..schema import Schema
from ..user import User

if PY3:
    from typing import Any, Dict, List


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
                properties_string = fields.pop('properties', None)
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

    # invitation
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
        if self.unregister_schema(invitation) is True:
            return self.register_schema(invitation)
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
            'properties': schema.stringified_properties,
        }
        if schema.display_name is not None:
            mapping['display_name'] = schema.display_name
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

    def register_message_box(self, message_box):
        """MessageBoxオブジェクトをストレージに登録する.

        :param MessageBox message_box: MessageBoxオブジェクト
        :return: 成功/失敗
        :rtype: bool
        """
        mapping = {
            'uuid': message_box.uuid,
            'schema_uuid': message_box.schema_uuid,
            'of_master': message_box.of_master
        }
        if message_box.display_name is not None:
            mapping['display_name'] = message_box.display_name
        if message_box.description is not None:
            mapping['description'] = message_box.description

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

    def register_module(self, module):
        """Moduleオブジェクトをストレージに登録する.

        :param Module module: Moduleオブジェクト
        :return: 成功/失敗
        :rtype: bool
        """
        mapping = {
            'uuid': module.uuid,
            'message_box_uuids': module.stringified_message_box_uuids,
            'tags': module.stringified_tags,
        }
        if module.display_name is not None:
            mapping['display_name'] = module.display_name
        if module.description is not None:
            mapping['description'] = module.description

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

    def _generate_uuid(self, model_class):
        while True:
            generated = uuid.uuid4()
            if not self.redis_client.exists(model_class.make_storage_key(generated)):
                break
        return generated

    def update_user_last_access(self, user_id, dt):
        """Userの最終アクセス時刻を記録する

        :param UUID user_id: UserのID
        :param datetime datetime.datetime: 最終アクセス時刻(UTC)
        :return: 成功/失敗
        :rtype: bool
        """
        assert isinstance(dt, datetime.datetime)

        dt = prepare_date(dt)
        self.redis_client.set(User.make_key_for_last_access(user_id), format_date(dt))
        print('update date', user_id, dt)

    def get_user_last_access(self, user_id):
        """Userの最終アクセス時刻を記録する

        :param UUID user_id: UserのID
        :return: 成功/失敗
        :rtype: datetime.datetime
        """
        val = self.redis_client.get(User.make_key_for_last_access(user_id))
        if not val:
            return None
        return prepare_date(val)
