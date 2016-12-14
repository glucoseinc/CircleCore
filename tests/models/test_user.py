# -*- coding: utf-8 -*-
import pytest

from circle_core.models import User


TEST_UUID1 = '6f7d25f0-54df-421c-b8a6-a491e37ba96d'
TEST_UUID2 = 'eb2ea238-a13f-4542-8de4-0f6b3a67fca6'


class TestUser(object):
    @pytest.mark.parametrize(('uuid', 'mail_address', 'encrypted_password', 'permissions', 'expected'), [
        (TEST_UUID1, 'test_manager@test.test',
         '$6$6f7d25f054df421cb8a6a491e37ba96d$63471d3b07234b307d3c6c59f65ef3b1415efaab1509ef'
         '1caa415e5ee80b8a13c4a488d117a30857cf34144ec504dd27c20c6fc641051a2707ea54aa0a302d99', 'admin',
         {'uuid': TEST_UUID1,
          'mail_address': 'test_manager@test.test',
          'password': 'manager',
          'permissions': ['admin'],
          'storage_key': 'user_{}'.format(TEST_UUID1),
          }),
        (TEST_UUID2, 'test_user@test.test',
         '$6$eb2ea238a13f45428de40f6b3a67fca6$fa83cbcc141436fefcad61838817caee601435115bed2c'
         'e1a4e313fa55a2d42241128533bf65563cade6fc43be2e0e3d44ef518d9cb39adde7a69e7001c9b53e', '',
         {'uuid': TEST_UUID2,
          'mail_address': 'test_user@test.test',
          'password': 'user',
          'permissions': [],
          'storage_key': 'user_{}'.format(TEST_UUID2),
          }),
    ])
    def test_init(self, uuid, mail_address, encrypted_password, permissions, expected):
        user = User(uuid, mail_address, encrypted_password, permissions)
        assert str(user.uuid) == expected['uuid']
        assert user.mail_address == expected['mail_address']
        assert user.is_password_matched(expected['password'])
        assert sorted(user.permissions) == sorted(expected['permissions'])
        assert user.storage_key == expected['storage_key']

    def test_is_key_matched(self):
        assert User.is_key_matched('user_{}'.format(TEST_UUID1)) is True
        assert User.is_key_matched('schema_{}'.format(TEST_UUID1)) is False
        assert User.is_key_matched('user') is False
        assert User.is_key_matched('user_test_manager@test.test') is False
