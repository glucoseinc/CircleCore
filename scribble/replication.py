import os
import re
import subprocess
import sys
import tempfile
from time import sleep
from uuid import UUID

from base58 import b58encode

from sqlalchemy import create_engine

import circle_core


def main(master_dir, slave_dir):
    master_dir = tempfile.mkdtemp('master')
    slave_dir = tempfile.mkdtemp('slave')
    # master_dir = str(tmpdir_factory.mktemp('master'))
    # slave_dir = str(tmpdir_factory.mktemp('slave'))
    # master_dir = os.path.abspath('tmp/master')
    # slave_dir = os.path.abspath('tmp/slave')
    ipc_prefix = 'ipc://{}/'.format(tempfile.gettempdir())

    # prepare database
    engine = create_engine('mysql+pymysql://root@localhost')
    engine.execute('DROP DATABASE IF EXISTS crcr_test_master')
    engine.execute('CREATE DATABASE crcr_test_master')
    engine.execute('DROP DATABASE IF EXISTS crcr_test_slave')
    engine.execute('CREATE DATABASE crcr_test_slave')

    # TODO: truncate all tables
    master_db_url = 'mysql+pymysql://root@localhost/crcr_test_master'
    slave_db_url = 'mysql+pymysql://root@localhost/crcr_test_slave'

    counter_py = os.path.abspath(os.path.join(circle_core.__package__, os.pardir, 'sample', 'sensor_counter.py'))
    assert os.path.exists(counter_py)

    # MetaDataSessionがシングルトンなのでCliRunnerを使うとslaveもmasterも同じmetadata.sqliteを読んでしまう
    # なので、masterとslaveのディレクトリを分ける...

    # master
    os.chdir(master_dir)
    with open('circle_core.ini', 'w') as config:
        config.write(
            """
[circle_core]
uuid = auto
prefix = {master_dir}
metadata_file_path = ${{prefix}}/metadata.sqlite
log_file_path = ${{prefix}}/core.log
hub_socket = {ipc_prefix}test_crcr_hub_master.ipc
request_socket = {ipc_prefix}test_crcr_req_master.ipc
db = {db_url}
log_dir = ${{prefix}}
time_db_dir = ${{prefix}}
cycle_time=3
cycle_count=20

[circle_core:http]
listen = 127.0.0.1
port = 5001
websocket = on
admin = on
admin_base_url = http://${{listen}}:${{port}}
skip_build = on
""".format(db_url=master_db_url, master_dir=master_dir, ipc_prefix=ipc_prefix)
        )

    result = subprocess.run(['crcr', 'module', 'add', '--name', 'counterbot'], check=True, stdout=subprocess.PIPE)
    module_uuid = re.search(r'^Module "([0-9A-Fa-f-]+)" is added\.$', result.stdout.decode(), re.MULTILINE).group(1)

    result = subprocess.run(
        ['crcr', 'schema', 'add', '--name', 'counterbot', 'count:int', 'body:string'],
        check=True,
        stdout=subprocess.PIPE
    )
    schema_uuid = re.search(r'^Schema "([0-9A-Fa-f-]+)" is added\.$', result.stdout.decode(), re.MULTILINE).group(1)

    # run master
    result = subprocess.run(
        ['crcr', 'box', 'add', '--name', 'counterbot', '--schema', schema_uuid, '--module', module_uuid],
        check=True,
        stdout=subprocess.PIPE
    )
    box_uuid = re.search(r'^MessageBox "([0-9A-Fa-f-]+)" is added\.$', result.stdout.decode(), re.MULTILINE).group(1)
    table_name = 'message_box_{}'.format(b58encode(UUID(box_uuid).bytes).decode('latin1'))

    result = subprocess.run(
        ['crcr', 'replication_link', 'add', '--name', 'slave1', '--all-boxes'], check=True, stdout=subprocess.PIPE
    )
    link_uuid = re.search(r'^Replication Link "([0-9A-Fa-f-]+)" is added\.$', result.stdout.decode(),
                          re.MULTILINE).group(1)

    # run master & counter
    running_master = subprocess.Popen(['crcr', '--debug', 'run'])
    sleep(1)

    bot = subprocess.Popen(
        [
            sys.executable,
            counter_py,
            '--box-id',
            box_uuid,
            '--to',
            '{ipc_prefix}/test_crcr_req_master.ipc'.format(ipc_prefix=ipc_prefix),
            '--interval',
            '0.2',
            '--silent',
        ],
    )

    # masterにデータを注入
    # masterのメッセージボックスが空の状態でレプリケーションを始めると以降受信したメッセージがslaveに転送されない
    try:
        bot.wait(timeout=3)
    except subprocess.TimeoutExpired:
        pass

    # データが投入されているかチェック
    assert (
        create_engine(master_db_url).connect().execute('SELECT _created_at, _counter FROM {}'.format(table_name)
                                                      ).fetchall()
    )

    # slave
    os.chdir(slave_dir)

    with open('circle_core.ini', 'w') as config:
        config.write(
            """
[circle_core]
uuid = auto
prefix = {slave_dir}
metadata_file_path = ${{prefix}}/metadata.sqlite
log_file_path = ${{prefix}}/core.log
hub_socket = {ipc_prefix}/test_crcr_hub_slave.ipc
request_socket = {ipc_prefix}/test_crcr_hub_slave.ipc
db = {db_url}
log_dir = ${{prefix}}
time_db_dir = ${{prefix}}
cycle_time=3
cycle_count=20

[circle_core:http]
listen = 127.0.0.1
port = 5002
websocket = on
admin = on
admin_base_url = http://${{listen}}:${{port}}
skip_build = on
""".format(db_url=slave_db_url, slave_dir=slave_dir, ipc_prefix=ipc_prefix)
        )

    subprocess.run(
        ['crcr', 'replication_master', 'add', '--endpoint', 'ws://localhost:5001/replication/{}'.format(link_uuid)],
        check=True
    )

    running_slave = subprocess.Popen(['crcr', '--debug', 'run'])

    try:
        bot.wait(timeout=10)
    except subprocess.TimeoutExpired:
        pass
    else:
        assert 0, 'bot closed unexpectedly'
    assert bot.returncode is None

    bot.terminate()
    sleep(10)  # masterがslaveにレプリケーションしきるための猶予
    running_master.terminate()
    running_slave.terminate()

    master_messages = frozenset(
        tuple(t) for t in create_engine(master_db_url).connect().
        execute('SELECT _created_at, _counter FROM {}'.format(table_name)).fetchall()
    )
    slave_messages = frozenset(
        tuple(t) for t in create_engine(slave_db_url).connect().
        execute('SELECT _created_at, _counter FROM {}'.format(table_name)).fetchall()
    )

    assert master_messages == slave_messages, 'missing messages : {}'.format(sorted(master_messages - slave_messages))


with tempfile.TemporaryDirectory() as master_dir, tempfile.TemporaryDirectory() as slave_dir:
    main(master_dir, slave_dir)
