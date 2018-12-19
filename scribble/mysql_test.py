import asyncio
import logging
import sys
import uuid

import tornado.ioloop

from circle_core.database import Database
from circle_core.logger import logger
from circle_core.message import ModuleMessage
from circle_core.models import MessageBox, MetaDataSession, Module, Schema
from circle_core.testing import setup_db
from circle_core.writer import JournalDBWriter, QueuedDBWriter, QueuedDBWriterDelegate


def _init_logging(debug=False):
    # if we are attached to tty, use colorful.
    fh = logging.StreamHandler(sys.stderr)
    try:
        from circle_core.logger import NiceColoredFormatter
        # 色指示子で9charsとる
        fh.setFormatter(NiceColoredFormatter('%(nice_levelname)-14s %(nice_name)-33s: %(message)s',))
    except ImportError:
        fh.setFormatter(logging.Formatter('%(levelname)-5s %(name)-24s: %(message)s',))

    root_logger = logging.getLogger()
    root_logger.addHandler(fh)
    root_logger.setLevel(logging.DEBUG if debug else logging.INFO)


done = False


async def countup():
    import time

    while not done:
        print(time.time())
        await asyncio.sleep(1)


async def test():
    counterloop = asyncio.ensure_future(countup())

    setup_db()

    mbox_id = uuid.UUID('49EB92A3-AAE8-43A1-BC43-B7933DE96C6A')
    with MetaDataSession.begin():
        schema = Schema.create(display_name='Schema', properties='x:int,y:float')
        module = Module.create(display_name='Module')
        mbox = MessageBox(uuid=mbox_id, schema_uuid=schema.uuid, module_uuid=module.uuid)
        MetaDataSession.merge(schema)
        MetaDataSession.merge(module)
        MetaDataSession.merge(mbox)

    database = Database(
        'mysql+pymysql://root:hogehoge@localhost/crcr_test',
        './tmp/',
        './tmp/',
        connect_args=dict(write_timeout=3, read_timeout=3)
    )
    database.drop_message_box(mbox)

    queued_writer = QueuedDBWriter(database, './tmp/')

    class Delegate(QueuedDBWriterDelegate):

        async def on_reconnect(self) -> None:
            print('on_reconnect')
            writer.touch()

    queued_writer = QueuedDBWriter(database, './tmp/', delegate=Delegate())
    writer = JournalDBWriter(queued_writer, './tmp/')

    print('connect')
    # input('> ')
    database.connect()

    print('store')
    # input('> ')
    message = ModuleMessage(mbox.uuid, 123456.789, 0, {'x': 1, 'y': 2})
    assert (await writer.store(mbox, message)) is True

    print('store2 , please shutdown mysql')
    await async_input('> ')

    message = ModuleMessage(mbox.uuid, 123457.0, 1, {'x': 3, 'y': 4})
    assert (await writer.store(mbox, message)) is True

    assert (await writer.store(mbox, ModuleMessage(mbox.uuid, 123458.0, 2, {'x': 4, 'y': 4}))) is True
    assert (await writer.store(mbox, ModuleMessage(mbox.uuid, 123459.0, 3, {'x': 5, 'y': 4}))) is True
    assert (await writer.store(mbox, ModuleMessage(mbox.uuid, 123460.0, 4, {'x': 6, 'y': 4}))) is True
    assert (await writer.store(mbox, ModuleMessage(mbox.uuid, 123461.0, 5, {'x': 7, 'y': 4}))) is True

    print('store3 , please wakeup mysql')
    await async_input('> ')

    logger.info('DONE!')
    global done
    done = True
    await counterloop


def async_input(*args):
    return tornado.ioloop.IOLoop.current().run_in_executor(None, input, *args)


_init_logging(True)
loop = tornado.ioloop.IOLoop.current()
loop.run_sync(test)
# asyncio.get_event_loop().run_until_complete(test())
