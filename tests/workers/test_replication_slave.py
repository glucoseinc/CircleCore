# # -*- coding: utf-8 -*-
# import json
# from threading import Thread
# from time import sleep, time
# from uuid import UUID
from unittest.mock import DEFAULT, MagicMock, Mock

import pytest

from sqlalchemy.sql.expression import select

# from sqlalchemy import Table, create_engine
# from sqlalchemy.engine.reflection import Inspector
# from sqlalchemy.types import DECIMAL, INTEGER

# from tornado.httpserver import HTTPServer
# from tornado.ioloop import IOLoop
# from tornado.web import Application
# from tornado.websocket import WebSocketHandler

# from websocket import WebSocketConnectionClosedException

# from circle_core import database
# from circle_core.database import Database
# # from circle_core.models import message
# # from circle_core.models.message import ModuleMessage
# # from circle_core.models.message_box import MessageBox
# # from circle_core.models.metadata.base import MetadataReader
# # from circle_core.models.module import Module
# # from circle_core.models.schema import Schema
# # from circle_core.server.ws import ModuleHandler, ReplicationMaster
# # from circle_core.workers import replication_slave
# # from circle_core.workers.replication_slave import ReplicationSlave
from circle_core.constants import MasterCommand, ReplicationState
from circle_core.database import Database
from circle_core.models import CcInfo, MessageBox, MetaDataSession, Module, ReplicationMaster, Schema, generate_uuid
from circle_core.workers.slave_driver import SlaveDriverWorker
from circle_core.writer import QueuedDBWriter

# # class DummyMetadata(object):
# #     schemas = [Schema('95eef02e-36e5-446e-9fea-aedd10321f6f', 'json', [{'name': 'hoge', 'type': 'int'}])]
# #     message_boxes = [
# #         MessageBox(
# #             '402a7a37-691d-40ed-b0fe-4aeed9d0bba1', '95eef02e-36e5-446e-9fea-aedd10321f6f',
# #             '314a578a-6543-4331-90f7-ed80c81d29bf', 'DummyMessageBox')
# #     ]
# #     modules = [
# #         Module('314a578a-6543-4331-90f7-ed80c81d29bf', 'DummyModule', 'foo,bar'),
# #     ]
# #     users = []
# #     replication_links = []
# #     cc_infos = []
# #     invitations = []
# #     parse_url_scheme = None
# #     writable = True
# #     prefix = getcwd()

# #     def register_schema(self, schema):  # TODO: こういうのをMockにするべきなのかな
# #         self.schemas.append(schema)

# #     def register_message_box(self, box):
# #         self.message_boxes.append(box)

# #     def register_module(self, module):
# #         self.modules.append(module)

# @pytest.mark.skip(reason='rewriting...')
# @pytest.mark.usefixtures('class_wide_mysql')
# class TestReplicationSlave:

#     @classmethod
#     def setup_class(cls):
#         replication_slave.get_uuid = lambda: '5c8fe778-1cb8-4a92-8f5d-588990a19def'
#         replication_slave.metadata = DummyMetadata
#         message.metadata = DummyMetadata
#         database.metadata = DummyMetadata

#     def teardown_method(self, method):
#         ioloop = IOLoop.current()
#         self.server.stop()
#         ioloop.add_callback(ioloop.stop)
#         self.thread.join()

#     def run_dummy_server(self, replication_master):

#         def run():
#             app = Application([(r'/replication/(?P<slave_uuid>[0-9A-Fa-f-]+)', replication_master)])
#             self.server = HTTPServer(app)
#             self.server.listen(5001)
#             IOLoop.current().start()

#         self.thread = Thread(target=run)
#         self.thread.daemon = True
#         self.thread.start()
#         sleep(1)

#     @pytest.mark.timeout(2)
#     def test_migrate(self):
#         DummyMetadata.database_url = self.mysql.url

#         class DummyReplicationMaster(WebSocketHandler):

#             def on_message(self, message):
#                 msg = json.loads(message)
#                 if msg == {'command': 'MIGRATE'}:
#                     res = json.dumps({
#                         'crcr_uuid':
#                         '1f479ba2-5642-41bf-8661-f52abb09e5b5',
#                         'modules': [{
#                             'uuid': '8e654793-5c46-4721-911e-b9d19f0779f9',
#                             'message_box_uuids': ['316720eb-84fe-43b3-88b7-9aad49a93220'],
#                             'display_name': 'DummyModule',
#                             'tags': 'foo,bar'
#                         }],
#                         'message_boxes': [{
#                             'uuid': '316720eb-84fe-43b3-88b7-9aad49a93220',
#                             'display_name': 'DummyMessageBox',
#                             'schema_uuid': '44ae2fd8-52d0-484d-9a48-128b07937a0a'
#                         }],
#                         'schemas': [{
#                             'uuid': '44ae2fd8-52d0-484d-9a48-128b07937a0a',
#                             'display_name': 'DummySchema',
#                             'properties': [{
#                                 'name': 'hoge',
#                                 'type': 'int'
#                             }]
#                         }]
#                     })
#                     self.write_message(res)

#         self.run_dummy_server(DummyReplicationMaster)

#         slave = ReplicationSlave(DummyMetadata, 'localhost:5001', [])
#         req = json.dumps({'command': 'MIGRATE'})
#         slave.ws.send(req)
#         slave.migrate()

#         # Redisに同期親の情報が書き込まれているか
#         assert filter(
#             lambda schema: schema.uuid == UUID('8e654793-5c46-4721-911e-b9d19f0779f9'), DummyMetadata.schemas)
#         assert filter(
#             lambda box: box.uuid == UUID('316720eb-84fe-43b3-88b7-9aad49a93220'), DummyMetadata.message_boxes)
#         assert filter(
#             lambda module: module.uuid == UUID('8e654793-5c46-4721-911e-b9d19f0779f9'), DummyMetadata.modules)
#         db = Database(self.mysql.url)
#         engine = create_engine(self.mysql.url)
#         inspector = Inspector.from_engine(engine)
#         box = MessageBox(
#             '316720eb-84fe-43b3-88b7-9aad49a93220', '44ae2fd8-52d0-484d-9a48-128b07937a0a', 'DummyMessageBox'
#         )
#         table_name = db.make_table_name_for_message_box(box)
#         columns = inspector.get_columns(table_name)
#         types = {'_created_at': DECIMAL, '_counter': INTEGER, 'hoge': INTEGER}

#         # DBのテーブルが同期されているか
#         for column in columns:
#             assert isinstance(column['type'], types[column['name']])

#     @pytest.mark.timeout(3)
#     def test_receive(self):
#         now = time()

#         class DummyReplicationMaster(WebSocketHandler):

#             def on_message(self, req):
#                 req = json.loads(req)
#                 if req['command'] == 'RECEIVE':
#                     for count in range(10):
#                         resp = json.dumps({
#                             'module_uuid': '8e654793-5c46-4721-911e-b9d19f0779f9',
#                             'box_id': '316720eb-84fe-43b3-88b7-9aad49a93220',
#                             'timestamp': now,
#                             'count': count,
#                             'payload': {
#                                 'hoge': 123
#                             }
#                         })
#                         self.write_message(resp)

#                     raise RuntimeError('This exception is used to stop DummyReplicationMaster.')

#         self.run_dummy_server(DummyReplicationMaster)

#         slave = ReplicationSlave(DummyMetadata, 'localhost:5001', [])
#         req = json.dumps({'command': 'RECEIVE'})
#         slave.ws.send(req)
#         with pytest.raises(WebSocketConnectionClosedException):
#             slave.receive()

#         db = Database(self.mysql.url)
#         table = Table('message_box_76pzhAbUqxJeYp1CYkLBc3', db._metadata, autoload=True, autoload_with=db._engine)
#         session = db._session()

#         # テーブルにメッセージが書き込まれているか
#         with session.begin():
#             rows = session.query(table).all()
#             assert len(rows) == 10
#             assert ModuleMessage.is_equal_timestamp(rows[0]._created_at, now)
#             assert rows[0]._counter == 0
#             assert rows[0].hoge == 123


@pytest.mark.usefixtures('mock_circlecore')
@pytest.mark.usefixtures('mysql')
@pytest.mark.asyncio
async def test_replicate_blob(mysql, mock_circlecore):
    """BLOBをReplicateできるかテスト

    このテストは見ている範囲が広すぎるにしてはみたいところがみれてないのでは"""
    mock_cc = MagicMock()
    envdir = mock_circlecore[1]

    database = Database(mysql.url, time_db_dir=envdir, log_dir=envdir)

    with MetaDataSession.begin():
        master_uuid = generate_uuid(model=CcInfo)

        # ccinfo = CcInfo.query.filter_by(myself=True).one()
        master_cc_info = CcInfo(uuid=master_uuid, display_name='test master', myself=False, work='')
        replication_master = ReplicationMaster(endpoint_url='', info=master_cc_info)
        module = Module(uuid=generate_uuid(model=Module), cc_info=master_cc_info)
        schema = Schema.create(cc_uuid=master_cc_info.uuid, display_name='Schema', properties='x:int,y:float,data:blob')
        box = MessageBox(uuid=generate_uuid(model=MessageBox), schema=schema, module=module, display_name='Box')

        MetaDataSession.add(master_cc_info)
        MetaDataSession.add(replication_master)
        MetaDataSession.add(module)
        MetaDataSession.add(schema)
        MetaDataSession.add(box)

    async def dummy_store(*args):
        return DEFAULT

    slave_dirver = SlaveDriverWorker(mock_cc, '', False)
    slave_dirver.initialize()
    assert len(slave_dirver.replicators) == 1
    assert replication_master.id in slave_dirver.replicators

    replicator = slave_dirver.replicators[replication_master.id]
    replicator.state = ReplicationState.SYNCING
    replicator.target_boxes = {box.uuid: box}
    replicator.ws = MagicMock()

    writer = QueuedDBWriter(database, envdir)
    replicator.writer = writer

    datahash = (
        'bf3408132f944568dd02827441f8c69b1f3e5a36bd7693a7aeeffd490037b56d'
        '9ad9406892ecd70cb9c0d31a746e7e790e731ae491dc0176a49369a2a4044581'
    )
    replicator.ws.read_message = Mock(
        side_effect=make_dummy_read_message(
            '''\
{{
    "command": "new_message",
    "message": {{
        "boxId": "{box_id}",
        "timestamp": "1546006083.213117",
        "counter": 0,
        "payload": {{
            "x": 32768,
            "y": 3.14,
            "data": {{"$data": "{datahash}", "$source": "{source}", "$type": "text/plain"}}
        }}
    }}
}}
'''.format(box_id=str(box.uuid), datahash=datahash, source=master_cc_info.uuid)
        )
    )
    await replicator.wait_command((MasterCommand.NEW_MESSAGE,))

    replicator.ws.read_message.assert_called_once()

    with database._engine.begin() as connection:
        table = database.find_table_for_message_box(box)
        rows = connection.execute(select([table.c.data])).fetchall()

        assert len(rows) == 1
        expected = '{{"$data": "{datahash}", "$source": "{source}", "$type": "text/plain"}}' \
            .format(
                datahash=datahash,
                source=str(master_cc_info.uuid)
            )
        assert rows[0][0] == expected


def make_dummy_read_message(message):

    async def dummy():
        return message

    return dummy
