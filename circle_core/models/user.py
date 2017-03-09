# -*- coding: utf-8 -*-

"""User Model."""

# system module
import datetime
from hashlib import sha512
import random
import string

# community module
import sqlalchemy as sa
from sqlalchemy.ext.hybrid import hybrid_property

# project module
from circle_core.utils import format_date
from .base import generate_uuid, GUID, UUIDMetaDataBase


# type annotation
try:
    from typing import Dict, List, Optional, TYPE_CHECKING
    if TYPE_CHECKING:
        from uuid import UUID
except ImportError:
    pass


class User(UUIDMetaDataBase):
    """Userオブジェクト.

    :param UUID uuid: User UUID
    :param str account: アカウント名
    :param str _permissions: 権限
    :param List[str] permissions: 権限
    :param str work: 所属
    :param str mail_address: メールアドレス
    :param str telephone: 電話番号
    :param str encrypted_password: 暗号化パスワード
    :param datetime.datetime created_at: 作成日時
    :param datetime.datetime updated_at: 更新日時
    :param Optional[datetime.datetime] last_access_at: 最終アクセス日時
    """

    __tablename__ = 'users'

    uuid = sa.Column(GUID, primary_key=True)
    account = sa.Column(sa.String(255), nullable=False, unique=True)
    _permissions = sa.Column('permissions', sa.String(255))
    work = sa.Column(sa.Text, nullable=False, default='')
    mail_address = sa.Column(sa.Text, nullable=False, default='')
    telephone = sa.Column(sa.Text, nullable=False, default='')
    encrypted_password = sa.Column(sa.String(255), nullable=False)
    created_at = sa.Column(sa.DateTime, nullable=False, default=datetime.datetime.utcnow)
    updated_at = sa.Column(sa.DateTime, nullable=False, default=datetime.datetime.utcnow,
                           onupdate=datetime.datetime.utcnow)
    last_access_at = sa.Column(sa.DateTime, nullable=True)

    @classmethod
    def create(cls, **kwargs):
        """このモデルを作成する.

        :param Dict kwargs: キーワード引数
        :return: Userオブジェクト
        :rtype: User
        """
        return cls(
            uuid=generate_uuid(model=cls),
            **kwargs
        )

    def __init__(self, **kwargs):
        """init.

        :param Dict kwargs: キーワード引数
        """

        if 'password' in kwargs:
            if 'encrypted_password' in kwargs:
                raise ValueError('password and encrypted_password cannot set both at same time.')
            password = kwargs.pop('password')
            self.check_password(password)
            kwargs['encrypted_password'] = encrypt_password(password)

        super(User, self).__init__(**kwargs)

    def __repr__(self):
        """repr.

        :return: 文字列表現
        :rtype: str
        """
        return '<{module}.User {uuid} ({account})>'.format(
            module=__name__,
            uuid=self.uuid,
            account=self.account,
        )

    @hybrid_property
    def permissions(self):
        """権限リストを返す.

        :return: 権限リスト
        :rtype: List[str]
        """
        return self._permissions.split(',') if self._permissions else []

    @permissions.setter
    def permissions(self, permissions):
        """権限リストを更新する.

        :param List[str] permissions: 権限リスト
        """
        self._permissions = ','.join(permissions)

    def is_password_matched(self, password):
        """指定のパスワードがマッチしているか.

        :param str password:パスワード
        :return: マッチしているか
        :rtype: bool
        """
        return is_password_matched(password, self.encrypted_password)

    def is_admin(self):
        """ユーザがadmin権限をもっているかどうか.
        :return: adminであればTrue
        :rtype: bool
        """
        return 'admin' in self.permissions

    @classmethod
    def check_password(cls, password):
        """パスワードのvalidateを行う.

        :param password:
        """
        if len(password) < 6:
            raise ValueError('パスワードは6文字以上にしてください')

    def set_password(self, new_password):
        """パスワードを更新する.

        :param new_password: パスワード
        """
        self.check_password(new_password)
        self.encrypted_password = encrypt_password(new_password)

    def to_json(self, full=False):
        """このモデルのJSON表現を返す.

        :param bool full: 全ての情報を含めるか
        :return: JSON表現のDict
        :rtype: Dict
        """
        d = {
            'uuid': str(self.uuid),
            'account': self.account,
            'work': self.work,
            'mailAddress': self.mail_address,
            'telephone': self.telephone,
            'permissions': self.permissions,
            'createdAt': format_date(self.created_at),
            'updatedAt': format_date(self.updated_at),
            'lastAccessAt': format_date(self.last_access_at),
        }
        if full:
            d['encryptedPassword'] = self.encrypted_password

        return d

    def update_from_json(self, jsonobj):
        """JSON表現からモデルを更新する.

        :param Dict jsonobj: JSON表現のDict
        """
        for from_key, to_key in [
                ('account', 'account'), ('mailAddress', 'mail_address'), ('work', 'work'), ('telephone', 'telephone'),
                ('permissions', 'permissions')]:
            if from_key in jsonobj:
                setattr(self, to_key, jsonobj[from_key])

        if 'newPassword' in jsonobj:
            self.set_password(jsonobj['newPassword'])


def encrypt_password(password, salt=None):
    """パスワードを暗号化する.

    :param str password:パスワード
    :param str salt:SALT
    :return: 暗号化パスワード
    :rtype: str
    """
    if not salt:
        # generate salt
        salt = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(32))
        assert '$' not in salt

    hashed = sha512((salt + password).encode('utf-8')).hexdigest()
    return '$6${}${}'.format(salt, hashed)


def is_password_matched(test, encrypted):
    """平文パスワードが暗号化パスワードにマッチしているか.

    :param str test:平文パスワード
    :param str encrypted: 暗号化パスワード
    :return: マッチしているか
    :rtype: bool
    """
    try:
        _, six, salt, hashed = encrypted.split('$')
        if six != '6':
            raise ValueError('invalid encrypted password')
    except ValueError:
        raise ValueError('invalid encrypted password')

    return sha512((salt + test).encode('utf-8')).hexdigest() == hashed
