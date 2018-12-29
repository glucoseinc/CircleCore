# -*- coding: utf-8 -*-
import asyncio
import decimal
import json
import os
import uuid
from unittest.mock import MagicMock

import pytest

from circle_core.message import ModuleMessage
from circle_core.models import MessageBox, MetaDataSession, Module, Schema
from circle_core.testing import mock_circlecore_context
from circle_core.writer.journal_writer import JournalDBWriter, JournalReader


@pytest.fixture()
def dummy_mbox():
    print("            setup before function")

    with mock_circlecore_context():

        mbox_id = uuid.uuid4()
        with MetaDataSession.begin():
            schema = Schema.create(display_name='Schema', properties='x:int,y:float')
            module = Module.create(display_name='Module')
            mbox = MessageBox(uuid=mbox_id, schema_uuid=schema.uuid, module_uuid=module.uuid)
            MetaDataSession.add(schema)
            MetaDataSession.add(module)
            MetaDataSession.add(mbox)

        yield (schema, module, mbox)


@pytest.mark.asyncio
async def test_journal_db_writer(tmpdir, dummy_mbox, caplog):
    schema, module, mbox = dummy_mbox

    import logging
    caplog.set_level(logging.DEBUG)
    # check dir is empty
    assert not os.listdir(tmpdir)

    # open writer
    child_writer_mock = MagicMock()
    writer = JournalDBWriter(child_writer_mock, tmpdir)

    files = os.listdir(tmpdir)
    assert 'journal.pos' in files
    assert open(os.path.join(tmpdir, 'journal.pos'), 'rt').read() == ''

    # store message
    message = ModuleMessage(mbox.uuid, 123456.789, 0, {'x': 1, 'y': 2})
    child_writer_mock.store.side_effect = asyncio.coroutine(lambda *args, **kwargs: True)
    await writer.store(mbox, message)
    await asyncio.sleep(0.1)
    await writer.close()
    del writer

    files = os.listdir(tmpdir)
    assert 'journal.000' in files
    assert 'journal.pos' in files

    ln = open(os.path.join(tmpdir, 'journal.000')).read()
    assert ln.endswith('\n')
    assert ln and json.loads(ln) == {
        'boxId': mbox.uuid.hex,
        'timestamp': '123456.7890000000',
        'counter': 0,
        'payload': {
            'x': 1,
            'y': 2
        }
    }
    child_writer_mock.store.assert_called_once()
    checkpoint = '0\n{}'.format(len(ln))
    assert open(os.path.join(tmpdir, 'journal.pos')).read() == checkpoint

    # re-start journal
    child_writer_mock.store.side_effect = asyncio.coroutine(lambda *args, **kwargs: False)

    writer = JournalDBWriter(child_writer_mock, tmpdir)

    message = ModuleMessage(mbox.uuid, 123500.789, 1, {'x': 3, 'y': 4})
    await writer.store(mbox, message)
    await asyncio.sleep(0.1)
    await writer.close()
    del writer

    with open(os.path.join(tmpdir, 'journal.000')) as fp:
        ln = fp.readline()
        assert ln and json.loads(ln) == {
            'boxId': mbox.uuid.hex,
            'timestamp': '123456.7890000000',
            'counter': 0,
            'payload': {
                'x': 1,
                'y': 2
            }
        }

        ln = fp.readline()
        assert ln and json.loads(ln) == {
            'boxId': mbox.uuid.hex,
            'timestamp': '123500.7890000000',
            'counter': 1,
            'payload': {
                'x': 3,
                'y': 4
            }
        }

    print(child_writer_mock.store.call_args)
    print(child_writer_mock.store.call_args[0])
    assert child_writer_mock.store.call_count == 2
    assert child_writer_mock.store.call_args[0][1].timestamp == decimal.Decimal('123500.7890000000')
    assert open(os.path.join(tmpdir, 'journal.pos')).read() == checkpoint


@pytest.mark.asyncio
async def test_journal_reader(tmpdir):
    pos_file_path = os.path.join(tmpdir, 'journal.pos')

    # prepare test data
    with open(os.path.join(tmpdir, 'journal.000'), 'wt') as fp:
        for x in range(5):
            fp.write('{{"x": {}}}\n'.format(x))

    with open(os.path.join(tmpdir, 'journal.001'), 'wt') as fp:
        for x in range(100, 105):
            fp.write('{{"x": {}}}\n'.format(x))

    assert not os.path.exists(pos_file_path)
    reader = JournalReader(os.path.join(tmpdir, 'journal'))

    # 読み込める
    async with reader.read() as data:
        assert data == '{"x": 0}\n'
    assert os.path.exists(pos_file_path)
    assert open(pos_file_path).read() == '0\n9'

    # posが進んでいる
    async with reader.read() as data:
        assert data == '{"x": 1}\n'
        assert open(pos_file_path).read() == '0\n9'
    assert open(pos_file_path).read() == '0\n18'

    # 例外が起きたらposが進まない
    try:
        async with reader.read() as data:
            assert data == '{"x": 2}\n'
            raise Exception
    except Exception:
        pass
    assert open(pos_file_path).read() == '0\n18'

    # 同じ位置のものが読み込める
    async with reader.read() as data:
        assert data == '{"x": 2}\n'
    assert open(pos_file_path).read() == '0\n27'

    async with reader.read() as data:
        assert data == '{"x": 3}\n'
    assert open(pos_file_path).read() == '0\n36'

    async with reader.read() as data:
        assert data == '{"x": 4}\n'
    assert open(pos_file_path).read() == '0\n45'

    # 次のログファイルを読む
    async with reader.read() as data:
        assert data == '{"x": 100}\n'
    assert open(pos_file_path).read() == '1\n11'

    async with reader.read() as data:
        assert data == '{"x": 101}\n'
    async with reader.read() as data:
        assert data == '{"x": 102}\n'
    async with reader.read() as data:
        assert data == '{"x": 103}\n'
    async with reader.read() as data:
        assert data == '{"x": 104}\n'
    async with reader.read() as data:
        assert data is None


@pytest.mark.asyncio
async def test_rotate_journal(tmpdir, dummy_mbox, caplog):
    schema, module, mbox = dummy_mbox

    import logging
    caplog.set_level(logging.DEBUG)

    # prepare test data
    pos_file_path = os.path.join(tmpdir, 'journal.pos')

    for log_index in range(10):
        log_file_path = os.path.join(tmpdir, 'journal.{:03d}'.format(log_index))
        with open(log_file_path, 'wt') as fp:
            for x in range(5):
                fp.write('{{"x": {}}}\n'.format(x))

    with open(pos_file_path, 'wt') as fp:
        log_file_path = os.path.join(tmpdir, 'journal.{:03d}'.format(log_index))
        fp.write('{}\n{}'.format(log_index, os.stat(log_file_path).st_size))

    before_files = os.listdir(tmpdir)
    assert len(before_files) == 11

    # open writer
    child_writer_mock = MagicMock()
    child_writer_mock.store.side_effect = asyncio.coroutine(lambda *args, **kwargs: True)
    writer = JournalDBWriter(child_writer_mock, tmpdir, max_log_file_size=20)

    message = ModuleMessage(mbox.uuid, 123456.789, 0, {'x': 1, 'y': 2})
    await writer.store(mbox, message)
    await asyncio.sleep(0.1)

    #
    after_files = os.listdir(tmpdir)

    print(before_files)
    print(after_files)

    after_files.sort()
    assert after_files == ['journal.011', 'journal.pos']

    await writer.close()
    del writer
