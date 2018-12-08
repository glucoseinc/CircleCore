# -*- coding: utf-8 -*-

# system module
import os

# community module
import pytest
import sqlalchemy as sa
from sqlalchemy.engine.url import make_url
import tcptest.redis

# project module
from circle_core.models import MetaDataBase, MetaDataSession
from tests import crcr_uuid


@pytest.fixture()
def clear_metadata(request):
    path = './tmp/metadata.sqlite'

    def _clear_file():
        if os.path.exists(path):
            os.remove(path)

    _clear_file()
    request.addfinalizer(_clear_file)


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
    database_url = os.getenv('CRCR_TEST_DATABASE_URL', 'mysql+mysqlconnector://root@localhost/crcr_test')

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
    database_url = os.getenv('CRCR_TEST_DATABASE_URL', 'mysql+mysqlconnector://root@localhost/crcr_test')

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
