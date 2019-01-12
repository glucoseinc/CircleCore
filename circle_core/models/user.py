# -*- coding: utf-8 -*-
"""User Model."""

# system module
import base64
import datetime
import random
import string
from hashlib import sha512
from typing import Any, Dict, List, Optional, TYPE_CHECKING, cast

# community module
import sqlalchemy as sa
import sqlalchemy.orm.query
from sqlalchemy.ext.hybrid import hybrid_property

# project module
from circle_core.utils import format_date

from .base import GUID, MetaDataSession, UUIDMetaDataBase, generate_uuid

# type annotation
if TYPE_CHECKING:
    from uuid import UUID

    from mypy_extensions import TypedDict

    class UserJson(TypedDict, total=False):
        uuid: str
        account: str
        work: str
        mailAddress: str
        telephone: str
        permissions: List[str]
        createdAt: str
        updatedAt: str
        lastAccessAt: Optional[str]
        token: Optional[str]

TOKEN_BYTES = 128


class UserQuery(sqlalchemy.orm.query.Query):
    def filter_by_encoded_token(self, encoded_token):
        return self.filter_by(token=base64.b64decode(encoded_token))


class User(UUIDMetaDataBase):
    """Userオブジェクト.

    Attributes:
        last_access_at: 最終アクセス日時
        permissions: 権限
        uuid: User UUID
        _permissions: 権限
    :param str account: アカウント名
    :param str work: 所属
    :param str mail_address: メールアドレス
    :param str telephone: 電話番号
    :param str encrypted_password: 暗号化パスワード
    :param datetime.datetime created_at: 作成日時
    :param datetime.datetime updated_at: 更新日時
    """
    last_access_at: Optional[datetime.datetime]
    uuid: 'UUID'
    permissions: List[str]
    _permissions: str

    __tablename__ = 'users'
    query = MetaDataSession.query_property(UserQuery)

    uuid = sa.Column(GUID, primary_key=True)
    account = sa.Column(sa.String(255), nullable=False, unique=True)
    _permissions = sa.Column('permissions', sa.String(255))
    work = sa.Column(sa.Text, nullable=False, default='')
    mail_address = sa.Column(sa.Text, nullable=False, default='')
    telephone = sa.Column(sa.Text, nullable=False, default='')
    encrypted_password = sa.Column(sa.String(255), nullable=False)
    token = sa.Column(sa.Binary(128))
    created_at = sa.Column(sa.DateTime, nullable=False, default=datetime.datetime.utcnow)
    updated_at = sa.Column(
        sa.DateTime, nullable=False, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow
    )
    last_access_at = sa.Column(sa.DateTime, nullable=True)

    @classmethod
    def create(cls, **kwargs: Dict[str, Any]):
        """このモデルを作成する.

        :param Dict kwargs: キーワード引数
        :return: Userオブジェクト
        :rtype: User
        """
        return cls(uuid=generate_uuid(model=cls), **kwargs)

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

    @permissions.setter  # type: ignore
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
    def check_password(cls, password: str):
        """パスワードのvalidateを行う.

        :param password:
        """
        if len(password) < 6:
            raise ValueError('パスワードは6文字以上にしてください')

    def set_password(self, new_password: str):
        """パスワードを更新する.

        :param new_password: パスワード
        """
        self.check_password(new_password)
        self.encrypted_password = encrypt_password(new_password)

    @property
    def encoded_token(self):
        return base64.b64encode(self.token).decode('latin1') if self.token else None

    def renew_token(self) -> None:
        """tokenを(再)生成する。
        tokenは128バイトのバイナリ
        """
        self.token = bytes(bytearray(random.getrandbits(8) for _ in range(TOKEN_BYTES)))

    def to_json(self, full: bool = False) -> 'UserJson':
        """このモデルのJSON表現を返す.

        :param bool full: 全ての情報を含めるか
        :return: JSON表現のDict
        :rtype: Dict
        """
        d: 'UserJson' = {
            'uuid': str(self.uuid),
            'account': self.account,
            'work': self.work,
            'mailAddress': self.mail_address,
            'telephone': self.telephone,
            'permissions': self.permissions,
            'createdAt': cast(str, format_date(self.created_at)),
            'updatedAt': cast(str, format_date(self.updated_at)),
            'lastAccessAt': format_date(self.last_access_at),
            'token': None,
        }
        if full:
            d['token'] = self.encoded_token

        return d

    def update_from_json(self, jsonobj: Dict[str, Any]) -> None:
        """JSON表現からモデルを更新する.

        Args:
            jsonobj: JSON表現のDict
        """
        for from_key, to_key in [
            ('account', 'account'), ('mailAddress', 'mail_address'), ('work', 'work'), ('telephone', 'telephone'),
            ('permissions', 'permissions')
        ]:
            if from_key in jsonobj:
                setattr(self, to_key, jsonobj[from_key])

        if 'newPassword' in jsonobj:
            self.set_password(jsonobj['newPassword'])


def encrypt_password(password: str, salt: Optional[str] = None) -> str:
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


def is_password_matched(test: str, encrypted: str) -> bool:
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
