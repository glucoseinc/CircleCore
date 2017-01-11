# -*- coding: utf-8 -*-

"""User Model."""

# system module
from hashlib import sha512
import re
from uuid import UUID

# community module
from six import PY3

if PY3:
    from typing import List, Union


class UserError(Exception):
    pass


class User(object):
    """Userオブジェクト.

    :param UUID uuid: User UUID
    :param str mail_address: メールアドレス
    :param str encrypted_password: 暗号化パスワード
    :param List[str] permissions: 権限
    """

    def __init__(self, uuid, mail_address, encrypted_password, permissions=''):
        """init.

        :param Union[str, UUID] uuid: User UUID
        :param str mail_address: メールアドレス
        :param str encrypted_password: 暗号化パスワード
        :param str permissions: 権限
        """
        if not isinstance(uuid, UUID):
            try:
                uuid = UUID(uuid)
            except ValueError:
                raise UserError('Invalid uuid : {}'.format(uuid))

        self.uuid = uuid
        self.mail_address = mail_address
        self.encrypted_password = encrypted_password
        self.permissions = []
        for permission in permissions.split(','):
            stripped = permission.strip()
            if len(stripped):
                self.permissions.append(stripped)

    @property
    def stringified_permissions(self):
        """権限を文字列化する.

        :return: 文字列化権限
        :rtype: str
        """
        return ','.join(self.permissions)

    @property
    def storage_key(self):
        """ストレージキー.

        :return: ストレージキー
        :rtype: str
        """
        return 'user_{}'.format(self.uuid)

    @classmethod
    def is_key_matched(cls, key):
        """指定のキーがストレージキーの形式にマッチしているか.

        :param str key:
        :return: マッチしているか
        :rtype: bool
        """
        pattern = r'^user_[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$'
        return re.match(pattern, key) is not None

    def is_password_matched(self, password):
        """指定のパスワードがマッチしているか.

        :param str password:パスワード
        :return: マッチしているか
        :rtype: bool
        """
        return self.encrypted_password == encrypt_password(password, self.uuid.hex)

    def is_admin(self):
        """ユーザがadmin権限をもっているかどうか
        :return: adminであればTrue
        :rtype: bool
        """
        return 'admin' in self.permissions


def encrypt_password(password, salt):
    """パスワードを暗号化する.

    :param str password:パスワード
    :param str salt:SALT
    :return: 暗号化パスワード
    :rtype: str
    """
    hashed = sha512((salt + password).encode('utf-8')).hexdigest()
    return '$6${}${}'.format(salt, hashed)
