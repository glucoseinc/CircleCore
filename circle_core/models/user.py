# -*- coding: utf-8 -*-

"""User Model."""

# system module
from hashlib import sha512
import re
from uuid import UUID

# community module
from six import PY3

from circle_core.utils import format_date, prepare_date


if PY3:
    from typing import List, Union


class UserError(Exception):
    pass


class User(object):
    """Userオブジェクト.

    :param UUID uuid: User UUID
    :param str account: アカウント
    :param List[str] permissions: 権限
    :param str work: 所属
    :param str mail_address: メールアドレス
    :param str telephone: 電話番号
    :param str encrypted_password: 暗号化パスワード
    :param datetime.datetime date_last_access: 最終アクセス時刻
    """

    def __init__(
            self, uuid, account, permissions, work, mail_address, telephone,
            encrypted_password=None, password=None, date_last_access=None):
        """init.

        :param Union[str, UUID] uuid: User UUID
        :param str account: アカウント
        :param List[str] permissions: 権限
        :param str work: 所属
        :param str mail_address: メールアドレス
        :param str telephone: 電話番号
        :param str encrypted_password: 暗号化パスワード
        :param str password: パスワード
        """
        assert uuid
        assert (password or encrypted_password) and not (password and encrypted_password)

        if not isinstance(uuid, UUID):
            try:
                uuid = UUID(uuid)
            except ValueError:
                raise UserError('Invalid uuid : {}'.format(uuid))

        if isinstance(permissions, str):
            permissions = permissions.split(',') if permissions else []
            permissions = list(set(x.strip() for x in permissions))

        if password:
            encrypted_password = encrypt_password(password, uuid.hex)

        self.uuid = uuid
        self.account = account
        self.mail_address = mail_address
        self.encrypted_password = encrypted_password
        self.permissions = permissions
        self.work = work
        self.mail_address = mail_address
        self.telephone = telephone
        self.date_last_access = prepare_date(date_last_access)

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

    @classmethod
    def make_key_for_last_access(cls, uuid):
        """指定のキーがストレージキーの形式にマッチしているか.

        :param str key:
        :return: マッチしているか
        :rtype: bool
        """
        return 'user_{}:last_access'.format(uuid)

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

    def set_password(self, new_password):
        assert self.uuid
        self.encrypted_password = encrypt_password(new_password, self.uuid.hex)

    def to_json(self, full=False):
        """このモデルのJSON表現を返す

        :return: json表現のdict
        :rtype: dict
        """
        d = {
            'uuid': str(self.uuid),
            'account': self.account,
            'work': self.work,
            'mailAddress': self.mail_address,
            'telephone': self.telephone,
            'permissions': self.permissions,
            'dateLastAccess': format_date(self.date_last_access)
        }
        if full:
            d['encrypted_password'] = self.encrypted_password

        return d

    @classmethod
    def from_json(cls, jsonobj):
        return cls(
            jsonobj['uuid'],
            jsonobj['account'],
            jsonobj['permissions'],
            jsonobj['work'],
            jsonobj['mailAddress'],
            jsonobj['telephone'],
            encrypted_password=jsonobj['encrypted_password'],
        )


def encrypt_password(password, salt):
    """パスワードを暗号化する.

    :param str password:パスワード
    :param str salt:SALT
    :return: 暗号化パスワード
    :rtype: str
    """
    hashed = sha512((salt + password).encode('utf-8')).hexdigest()
    return '$6${}${}'.format(salt, hashed)
