# -*- coding: utf-8 -*-

import os

import pytest
import redis
import tcptest.redis


@pytest.fixture(autouse=True, scope='session')
def redis_server(request):
    server = tcptest.redis.Server()
    server.start()

    os.environ['CRCR_CONFIG'] = 'redis://localhost:{}/0'.format(server.port)
    os.environ['CRCR_UUID'] = '00000000-1111-2222-3333-444444444444'

    def stop():
        server.stop()
    request.addfinalizer(stop)

    return server


@pytest.fixture()
def flushall_redis_server(redis_server):
    redis.Redis(port=redis_server.port).flushall()


@pytest.fixture()
def remove_environ(request):
    crcr_config = os.environ.pop('CRCR_CONFIG')
    crcr_uuid = os.environ.pop('CRCR_UUID')

    def at_exit():
        os.environ['CRCR_CONFIG'] = crcr_config
        os.environ['CRCR_UUID'] = crcr_uuid

    request.addfinalizer(at_exit)
