# -*- coding: utf-8 -*-

import os

import pytest
import redis
import sqlalchemy as sa
from sqlalchemy.engine.url import make_url
import tcptest.redis


@pytest.fixture(autouse=True, scope='session')
def redis_server(request):
    server = tcptest.redis.Server()
    server.start()

    os.environ['CRCR_METADATA'] = 'redis://localhost:{}/0'.format(server.port)
    os.environ['CRCR_UUID'] = '00000000-1111-2222-3333-444444444444'
    os.environ['CRCR_LOG_FILE_PATH'] = '/tmp/test_log.ltsv'

    def stop():
        server.stop()
    request.addfinalizer(stop)

    return server


@pytest.fixture()
def flushall_redis_server(redis_server):
    redis.Redis(port=redis_server.port).flushall()


@pytest.fixture()
def remove_environ(request):
    crcr_metadata = os.environ.pop('CRCR_METADATA')
    crcr_uuid = os.environ.pop('CRCR_UUID')
    crcr_log_file_path = os.environ.pop('CRCR_LOG_FILE_PATH')

    def at_exit():
        os.environ['CRCR_METADATA'] = crcr_metadata
        os.environ['CRCR_UUID'] = crcr_uuid
        os.environ['CRCR_LOG_FILE_PATH'] = crcr_log_file_path

    request.addfinalizer(at_exit)


@pytest.fixture()
def clear_log():
    crcr_log_file_path = os.environ.get('CRCR_LOG_FILE_PATH')
    if crcr_log_file_path is not None:
        if os.path.exists(crcr_log_file_path):
            os.remove(crcr_log_file_path)


@pytest.fixture(scope='function')
def mysql(request):
    """test DBをきれいにする
    """
    # from pytest_dbfixtures.utils import get_config
    database_url = os.getenv(
        'CRCR_TEST_DATABASE_URL',
        'mysql+mysqlconnector://root@localhost/crcr_test'
    )

    # database無しのをまず作る
    root_url = make_url(database_url)
    db = root_url.database
    root_url.database = None
    engine = sa.create_engine(root_url)

    with engine.begin() as conn:
        conn.execute('DROP DATABASE IF EXISTS `{db}`'.format(db=db))
        conn.execute('CREATE DATABASE `{db}`'.format(db=db))
        conn.execute('USE `{db}`'.format(db=db))

    def at_exit():
        with engine.begin() as conn:
            conn.execute('DROP DATABASE IF EXISTS `{db}`'.format(db=db))

    request.addfinalizer(at_exit)

    return sa.create_engine(database_url)


# クラスのメソッドでfixtureを使いたい。もっといい方法がありそう
@pytest.fixture(scope='class')
def class_wide_mysql(request):
    """test DBをきれいにする
    """
    # from pytest_dbfixtures.utils import get_config
    database_url = os.getenv(
        'CRCR_TEST_DATABASE_URL',
        'mysql+mysqlconnector://root@localhost/crcr_test'
    )

    # database無しのをまず作る
    root_url = make_url(database_url)
    db = root_url.database
    root_url.database = None
    engine = sa.create_engine(root_url)

    with engine.begin() as conn:
        conn.execute('DROP DATABASE IF EXISTS `{db}`'.format(db=db))
        conn.execute('CREATE DATABASE `{db}`'.format(db=db))
        conn.execute('USE `{db}`'.format(db=db))

    mysql = sa.create_engine(database_url)
    if request.cls is not None:
        request.cls.mysql = mysql

    yield mysql

    with engine.begin() as conn:
        conn.execute('DROP DATABASE IF EXISTS `{db}`'.format(db=db))
