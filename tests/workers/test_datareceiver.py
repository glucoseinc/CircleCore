from multiprocessing import Process
from time import sleep

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from circle_core import database
from circle_core.database import Database
from circle_core.helpers.nanomsg import Sender
from circle_core.helpers.topics import ModuleMessageTopic
from circle_core.models import message
from circle_core.models import MessageBox, Module, Schema
from circle_core.models.message import ModuleMessageFactory
from circle_core.models.metadata.base import MetadataReader


class DummyMetadata(MetadataReader):
    schemas = [Schema('95eef02e-36e5-446e-9fea-aedd10321f6f', 'json', [{'name': 'hoge', 'type': 'int'}])]
    message_boxes = [
        MessageBox(
            '402a7a37-691d-40ed-b0fe-4aeed9d0bba1', '95eef02e-36e5-446e-9fea-aedd10321f6f',
            '314a578a-6543-4331-90f7-ed80c81d29bf', 'DummyMessageBox1'),
        MessageBox(
            'dba1c788-69b4-4ca2-a7bd-8582eda96064', '95eef02e-36e5-446e-9fea-aedd10321f6f',
            None, 'DummyMessageBox2')
    ]
    modules = [
        Module('314a578a-6543-4331-90f7-ed80c81d29bf', 'DummyModule', 'foo,bar'),
    ]
    users = []
    invitations = []
    parse_url_scheme = None


def setup_module(module):
    message.metadata = DummyMetadata
    database.metadata = DummyMetadata


@pytest.mark.skip  # FIXME: 単体では通るが通しでやると通らない 前のテストで作られたSenderがここでも生きている...
@pytest.mark.timeout(3)
def test_specific_box(mysql):
    """メッセージが指定したメッセージボックスに格納されるか."""
    DummyMetadata.database_url = mysql.url
    db = Database(mysql.url)
    db.register_message_boxes(DummyMetadata.message_boxes, DummyMetadata.schemas)
    db.migrate()

    from circle_core.workers import datareceiver
    global worker
    worker = Process(target=lambda: datareceiver.run(DummyMetadata()))
    worker.daemon = True
    worker.start()

    topic = ModuleMessageTopic()
    sender = Sender(topic)
    messages = [
        ModuleMessageFactory.new('314a578a-6543-4331-90f7-ed80c81d29bf', {
            'hoge': 3,
            '_message_box': '402a7a37-691d-40ed-b0fe-4aeed9d0bba1'
        }) for _ in range(10)
    ]
    for msg in messages:
        sender.send([msg.encode()])
    sleep(2)

    table = db.find_table_for_message_box(msg.message_box)
    session = db._session()
    with session.begin():
        # 指定したメッセージボックスのテーブルに正しく書き込めているか
        rows = session.query(table).all()
        assert len(rows) == 10

        for row, msg in zip(rows, messages):
            assert row._created_at == msg.timestamp
            assert row._counter == msg.count
            assert row.hoge == 3

        # 指定していないメッセージボックスのテーブルに書き込んでいないか
        table = db.find_table_for_message_box(DummyMetadata.message_boxes[1])
        rows = session.query(table).all()
        assert len(rows) == 0


def teardown_module(module):
    global worker
    worker.terminate()
