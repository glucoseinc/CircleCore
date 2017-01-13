# -*- coding: utf-8 -*-

# system module
from __future__ import absolute_import

# community module
from redis import ConnectionError, Redis
from six import PY3

# project module
from .base import MetadataError, MetadataReader, MetadataWriter
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
                users.append(User(**fields))
        return users

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

    def register_user(self, user):
        """Userオブジェクトをストレージに登録する.

        :param User user: Userオブジェクト
        :return: 成功/失敗
        :rtype: bool
        """
        mapping = {
            'uuid': user.uuid,
            'mail_address': user.mail_address,
            'encrypted_password': user.encrypted_password,
            'permissions': user.stringified_permissions,
        }

        self.redis_client.hmset(user.storage_key, mapping)
        return True

    def unregister_user(self, user):
        """Userオブジェクトをストレージから削除する.

        :param User user: Userオブジェクト
        :return: 成功/失敗
        :rtype: bool
        """
        self.redis_client.delete(user.storage_key)
        return True
