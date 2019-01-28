import asyncio
import uuid

import pytest

from sqlalchemy.sql.expression import select

from circle_core.database import Database
from circle_core.message import ModuleMessage
from circle_core.models import MessageBox, MetaDataSession, Module, Schema


@pytest.mark.asyncio
async def test_post_date(mysql, mock_circlecore):
    mbox_id = uuid.uuid4()
    with MetaDataSession.begin():
        schema = Schema.create(display_name='Schema', properties='date:datetime,id1:float')
        module = Module.create(display_name='Module')
        mbox = MessageBox(uuid=mbox_id, schema_uuid=schema.uuid, module_uuid=module.uuid)
        MetaDataSession.add(schema)
        MetaDataSession.add(module)
        MetaDataSession.add(mbox)

    envdir = mock_circlecore[1]
    database = Database(mysql.url, time_db_dir=envdir, log_dir=envdir)
    journal_writer = database.make_writer()
    queued_writer = journal_writer.child_writer
    run_loop = asyncio.ensure_future(journal_writer.run())

    # post
    message = ModuleMessage(mbox.uuid, 123456.789, 0, {'date': '2017-09-01T24:00:00Z', 'id1': 3.14})
    await queued_writer.store(mbox, message)
    await queued_writer.flush()

    # close database
    await journal_writer.close()
    await run_loop

    with database._engine.begin() as connection:
        table = database.find_table_for_message_box(mbox)
        rows = connection.execute(select([table])).fetchall()
        assert len(rows) == 0
