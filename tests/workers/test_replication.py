import os
import re
import subprocess
import sys
from time import sleep
from uuid import UUID

from base58 import b58encode
from click.testing import CliRunner
import pytest
from sqlalchemy import create_engine

from circle_core.cli import cli_entry


def setup_module(module):
    terminate_crcr()


def teardown_module(module):
    terminate_crcr()


def terminate_crcr():
    subprocess.run("""ps x | grep crcr | grep -v grep | awk '{ system("kill "$1) }'""", shell=True, check=True)


def test_reproduce_missing_message(tmpdir_factory):
    master_dir = str(tmpdir_factory.mktemp('master'))
    os.chdir(master_dir)

    # prepare database
    engine = create_engine('mysql+mysqlconnector://root@localhost')
    engine.execute('DROP DATABASE IF EXISTS crcr_test_master')
    engine.execute('CREATE DATABASE crcr_test_master')
    engine.execute('DROP DATABASE IF EXISTS crcr_test_slave')
    engine.execute('CREATE DATABASE crcr_test_slave')

    # TODO: truncate all tables
    master_db_url = 'mysql+mysqlconnector://root@localhost/crcr_test_master'
    slave_db_url = 'mysql+mysqlconnector://root@localhost/crcr_test_slave'

    counter_py = os.path.abspath(os.path.join(
        os.path.dirname(__file__),
        os.pardir,
        os.pardir,
        'sample', 'sensor_counter.py'
    ))

    with open('circle_core.ini', 'w') as config:
        config.write("""
[circle_core]
uuid = auto
prefix = .
metadata_file_path = ${{prefix}}/metadata.sqlite
log_file_path = ${{prefix}}/core.log
hub_socket = ipc://${{prefix}}/crcr_hub.ipc
request_socket = ipc://${{prefix}}/crcr_request.ipc
db = {db_url}
time_db_dir = ${{prefix}}

[circle_core:http]
listen = 127.0.0.1
port = 5001
websocket = on
admin = on
admin_base_url = http://${{listen}}:${{port}}
skip_build = on
        """.format(db_url=master_db_url))

    # MetaDataSessionがシングルトンなのでCliRunnerを使うとslaveもmasterも同じmetadata.sqliteを読んでしまう
    running_master = subprocess.Popen(['crcr', '--debug', 'run'])
    sleep(1)

    result = subprocess.run(['crcr', 'module', 'add', '--name', 'counterbot'], check=True, stdout=subprocess.PIPE)
    module_uuid = re.search(r'^Module "([0-9A-Fa-f-]+)" is added\.$', result.stdout.decode(), re.MULTILINE).group(1)

    result = subprocess.run(
        ['crcr', 'schema', 'add', '--name', 'counterbot', 'count:int', 'body:string'],
        check=True,
        stdout=subprocess.PIPE
    )
    schema_uuid = re.search(r'^Schema "([0-9A-Fa-f-]+)" is added\.$', result.stdout.decode(), re.MULTILINE).group(1)

    result = subprocess.run([
        'crcr',
        'box',
        'add',
        '--name',
        'counterbot',
        '--schema',
        schema_uuid,
        '--module',
        module_uuid
    ], check=True, stdout=subprocess.PIPE)
    box_uuid = re.search(r'^MessageBox "([0-9A-Fa-f-]+)" is added\.$', result.stdout.decode(), re.MULTILINE).group(1)
    table_name = 'message_box_{}'.format(b58encode(UUID(box_uuid).bytes))

    bot = subprocess.Popen([
        sys.executable,
        counter_py,
        '--box-id', box_uuid,
        '--to', 'ipc://crcr_request.ipc',
        '--interval', '0.1'
    ])

    result = subprocess.run(
        ['crcr', 'replication_link', 'add', '--name', 'slave1', '--all-boxes'],
        check=True,
        stdout=subprocess.PIPE
    )
    link_uuid = re.search(
        r'^Replication Link "([0-9A-Fa-f-]+)" is added\.$',
        result.stdout.decode(),
        re.MULTILINE
    ).group(1)

    slave_dir = str(tmpdir_factory.mktemp('slave'))
    os.chdir(slave_dir)

    with open('circle_core.ini', 'w') as config:
        config.write("""
[circle_core]
uuid = auto
prefix = .
metadata_file_path = ${{prefix}}/metadata.sqlite
log_file_path = ${{prefix}}/core.log
hub_socket = ipc://${{prefix}}/crcr_hub.ipc
request_socket = ipc://${{prefix}}/crcr_request.ipc
db = {db_url}
time_db_dir = ${{prefix}}

[circle_core:http]
listen = 127.0.0.1
port = 5002
websocket = on
admin = on
admin_base_url = http://${{listen}}:${{port}}
skip_build = on
        """.format(db_url=slave_db_url))

    subprocess.run([
        'crcr',
        'replication_master',
        'add',
        '--endpoint',
        'ws://localhost:5001/replication/{}'.format(link_uuid)
    ], check=True)

    try:
        bot.wait(timeout=10)
    except subprocess.TimeoutExpired:
        pass

    # masterのメッセージボックスが空の状態でレプリケーションを始めると以降受信したメッセージがslaveに転送されない
    running_slave = subprocess.Popen(['crcr', '--debug', 'run'])

    try:
        bot.wait(timeout=20)
    except subprocess.TimeoutExpired:
        pass

    bot.terminate()
    sleep(10)  # masterがslaveにレプリケーションしきるための猶予
    running_master.terminate()
    running_slave.terminate()

    master_messages = frozenset(
        tuple(t) for t in create_engine(master_db_url)
        .connect()
        .execute('SELECT * FROM {}'.format(table_name))
        .fetchall()
    )
    slave_messages = frozenset(
        tuple(t) for t in create_engine(slave_db_url)
        .connect().execute('SELECT * FROM {}'.format(table_name))
        .fetchall()
    )

    assert master_messages == slave_messages, 'missing messages : {}'.format(master_messages - slave_messages)
