from unittest.mock import DEFAULT, MagicMock, Mock

import pytest

from circle_core.database import Database
from circle_core.models import MessageBox, MetaDataSession, Module, Schema, generate_uuid
from circle_core.workers.datareceiver import DataReceiverWorker


@pytest.mark.asyncio
@pytest.mark.usefixtures('mock_circlecore')
@pytest.mark.usefixtures('mysql')
async def test_datareceiver_store_blob(mock_circlecore, mysql, monkeypatch):
    metadata_db_engine, tmp_dir = mock_circlecore

    writer_mock = MagicMock()
    make_writer_mock = Mock(name='make_writer', return_value=writer_mock)

    async def dummy_store(*args, **kwargs):
        print('YEAH!!!!', repr((args, kwargs)))
        return DEFAULT

    writer_mock.store.side_effect = dummy_store

    monkeypatch.setattr(Database, 'make_writer', make_writer_mock)

    # make test schema/mbox
    with MetaDataSession.begin():
        schema = Schema.create(display_name='Schema', properties='x:int,y:float,data:blob')
        module = Module.create(display_name='Module')
        mbox = MessageBox(uuid=generate_uuid(model=MessageBox), schema_uuid=schema.uuid, module_uuid=module.uuid)

        MetaDataSession.add(schema)
        MetaDataSession.add(module)
        MetaDataSession.add(mbox)

    core_mock = MagicMock()
    worker = DataReceiverWorker(
        core_mock,
        'worker_key',
        db_url=mysql.url,
        time_db_dir=tmp_dir,
        log_dir=tmp_dir,
        cycle_time=10,
        cycle_count=10,
    )

    await worker.receive_new_message(mbox.uuid, {'x': 1, 'y': 2.0, 'data': 'data:text/plain;base64,aG9nZWhvZ2UK'})

    assert 0
