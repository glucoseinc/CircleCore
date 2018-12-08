# -*- coding: utf-8 -*-
import pytest

from circle_core.models import MetaDataSession, User
from circle_core.testing import setup_db


class TestUser(object):

    @classmethod
    def setup_class(cls):
        setup_db()

    @pytest.mark.parametrize(
        ('_input', 'expected'), [
            (
                dict(
                    account='admin',
                    password='password_admin',
                    _permissions='admin',
                    work='work_admin',
                    mail_address='admin@test.test',
                    telephone='1234567890'
                ),
                dict(
                    account='admin',
                    password='password_admin',
                    password_no_match='password_no_match',
                    permissions=['admin'],
                    work='work_admin',
                    mail_address='admin@test.test',
                    telephone='1234567890'
                )
            ),
        ]
    )
    def test_user(self, _input, expected):
        user = User.create(**_input)

        with MetaDataSession.begin():
            MetaDataSession.add(user)

        user = User.query.get(user.uuid)
        assert isinstance(user, User)
        assert user.account == expected['account']
        assert user.is_password_matched(expected['password']) is True
        assert user.is_password_matched(expected['password_no_match']) is False
        assert len(user.permissions) == len(expected['permissions'])
        for permission, exp_permission in zip(user.permissions, expected['permissions']):
            assert isinstance(permission, str)
            assert permission == exp_permission
        assert user.work == expected['work']
        assert user.mail_address == expected['mail_address']
        assert user.telephone == expected['telephone']

        assert user.is_admin() == ('admin' in expected['permissions'])

        jsonobj = user.to_json(full=True)
        assert str(user.uuid) == jsonobj['uuid']
        assert user.account == jsonobj['account']
        assert user.work == jsonobj['work']
        assert user.mail_address == jsonobj['mailAddress']
        assert user.telephone == jsonobj['telephone']
        assert len(user.permissions) == len(jsonobj['permissions'])
        for permission, exp_permission in zip(user.permissions, jsonobj['permissions']):
            assert permission == exp_permission
        assert user.encrypted_password == jsonobj['encryptedPassword']

    @pytest.mark.parametrize(
        ('old', 'new', 'expected'), [
            (
                dict(
                    account='oldAccount',
                    password='old_password',
                    work='old_work',
                    mail_address='old@test.test',
                    telephone='00000000000'
                ),
                dict(
                    account='newAccount',
                    newPassword='new_password',
                    work='new_work',
                    mailAddress='new@test.test',
                    telephone='99999999999'
                ),
                dict(
                    account='newAccount',
                    password='new_password',
                    work='new_work',
                    mail_address='new@test.test',
                    telephone='99999999999'
                )
            ),
        ]
    )
    def test_update_from_json(self, old, new, expected):
        user = User.create(**old)
        with MetaDataSession.begin():
            MetaDataSession.add(user)

        user = User.query.get(user.uuid)
        assert user.account != expected['account']
        assert user.is_password_matched(expected['password']) is False
        assert user.work != expected['work']
        assert user.mail_address != expected['mail_address']
        assert user.telephone != expected['telephone']

        user.update_from_json(new)
        with MetaDataSession.begin():
            MetaDataSession.add(user)

        user = User.query.get(user.uuid)
        assert user.account == expected['account']
        assert user.is_password_matched(expected['password']) is True
        assert user.work == expected['work']
        assert user.mail_address == expected['mail_address']
        assert user.telephone == expected['telephone']
