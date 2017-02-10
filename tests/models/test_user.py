# -*- coding: utf-8 -*-
import pytest

from circle_core.models import User


TEST_UUID1 = '6f7d25f0-54df-421c-b8a6-a491e37ba96d'
TEST_UUID2 = 'eb2ea238-a13f-4542-8de4-0f6b3a67fca6'


@pytest.mark.skip(reason='rewriting...')
class TestUser(object):
    @pytest.mark.parametrize(
        ('uuid', 'account', 'encrypted_password', 'permissions', 'work', 'mail_address', 'telephone', 'expected'),
        [(
            TEST_UUID1, 'test_manager',
            '$6$6f7d25f054df421cb8a6a491e37ba96d$63471d3b07234b307d3c6c59f65ef3b1415efaab1509ef'
            '1caa415e5ee80b8a13c4a488d117a30857cf34144ec504dd27c20c6fc641051a2707ea54aa0a302d99', 'admin',
            'workManager', 'test_manager@test.test', 'telManager',
            {
                'uuid': TEST_UUID1,
                'account': 'test_manager',
                'mail_address': 'test_manager@test.test',
                'password': 'manager',
                'permissions': ['admin'],
                'work': 'workManager',
                'telephone': 'telManager',
                'storage_key': 'user_{}'.format(TEST_UUID1),
            }
        ), (
            TEST_UUID2, 'test_user',
            '$6$eb2ea238a13f45428de40f6b3a67fca6$fa83cbcc141436fefcad61838817caee601435115bed2c'
            'e1a4e313fa55a2d42241128533bf65563cade6fc43be2e0e3d44ef518d9cb39adde7a69e7001c9b53e', '',
            'workUser', 'test_user@test.test', 'telUser',
            {
                'uuid': TEST_UUID2,
                'account': 'test_user',
                'mail_address': 'test_user@test.test',
                'password': 'user',
                'permissions': [],
                'work': 'workUser',
                'telephone': 'telUser',
                'storage_key': 'user_{}'.format(TEST_UUID2),
            }
        ),
        ])
    def test_init(self, uuid, account, encrypted_password, permissions, work, mail_address, telephone, expected):
        user = User(uuid, account, permissions, work, mail_address, telephone, encrypted_password=encrypted_password)

        assert str(user.uuid) == expected['uuid']
        assert user.account == expected['account']
        assert user.mail_address == expected['mail_address']
        assert user.is_password_matched(expected['password'])
        assert sorted(user.permissions) == sorted(expected['permissions'])
        assert user.work == expected['work']
        assert user.telephone == expected['telephone']
        assert user.storage_key == expected['storage_key']

    def test_is_key_matched(self):
        assert User.is_key_matched('user_{}'.format(TEST_UUID1)) is True
        assert User.is_key_matched('schema_{}'.format(TEST_UUID1)) is False
        assert User.is_key_matched('user') is False
        assert User.is_key_matched('user_test_manager@test.test') is False
