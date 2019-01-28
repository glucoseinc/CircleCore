# -*- coding: utf-8 -*-
import pytest

from sqlalchemy.sql.expression import select

from circle_core.database import Database
# from circle_core.exceptions import MigrationError
from circle_core.message import ModuleMessage
from circle_core.models import CcInfo, MessageBox, MetaDataSession, Module, Schema, generate_uuid
from circle_core.types import BlobMetadata

# TEST_SCHEMA_UUID = 'BAF7FDBB-FEA5-4364-8EC5-37FA579E381A'
# TEST_MODULE_UUID_1 = 'C7641AA8-32A7-47B8-8CCE-81C433081F59'

# test_schemas = [
#     Schema(
#         uuid=TEST_SCHEMA_UUID,
#         display_name='test schema',
#         properties=[
#             {
#                 'name': 'test_int',
#                 'type': 'int'
#             },
#             {
#                 'name': 'test_float',
#                 'type': 'float'
#             },
#             {
#                 'name': 'test_text',
#                 'type': 'text'
#             },
#         ],
#     )
# ]
# test_modules = [Module(uuid=TEST_MODULE_UUID_1, display_name='Test Module 1')]

# @pytest.mark.skip
# @pytest.mark.usefixtures('mysql')
# def test_migrate_new(mysql):
#     """宛先DBが空っぽなので、作成するだけのテスト"""
#     print('test test_migrate_new')
#     database = Database(mysql.url)
#     database.register_schemas_and_modules(test_schemas, test_modules)

#     result = database.check_tables()
#     assert len(result.new_tables) == 2
#     assert len(result.alter_tables) == 0
#     assert len(result.error_tables) == 0

#     database.migrate()

#     result = database.check_tables()
#     assert len(result.new_tables) == 0
#     assert len(result.alter_tables) == 0
#     assert len(result.error_tables) == 0

# @pytest.mark.skip
# @pytest.mark.usefixtures('mysql')
# def test_migrate_alter(mysql):
#     """宛先DBに変なスキーマかつ空のTableがあるのでrecreateするテスト"""
#     print('test test_migrate_alter')
#     with mysql.begin() as conn:
#         conn.execute('CREATE TABLE module_Rd4FHNG29WkSgBFEfqe3Kv (_created_at TIMESTAMP(6), hogehoge INTEGER);')

#     database = Database(mysql.url)
#     database.register_schemas_and_modules(test_schemas, test_modules)

#     result = database.check_tables()
#     assert len(result.new_tables) == 1
#     assert result.new_tables[0].name == 'meta'
#     assert len(result.alter_tables) == 1
#     assert result.alter_tables[0].name == 'module_Rd4FHNG29WkSgBFEfqe3Kv'
#     assert len(result.error_tables) == 0

#     database.migrate()

#     result = database.check_tables()
#     assert len(result.new_tables) == 0
#     assert len(result.alter_tables) == 0
#     assert len(result.error_tables) == 0

# @pytest.mark.skip
# @pytest.mark.usefixtures('mysql')
# def test_migrate_error(mysql):
#     """宛先DBに変なスキーマかつデータの入ったのTableがあるのでrエラーになるテスト"""
#     print('test test_migrate_error')
#     with mysql.begin() as conn:
#         conn.execute('CREATE TABLE module_Rd4FHNG29WkSgBFEfqe3Kv (_created_at TIMESTAMP(6), hogehoge INTEGER);')
#         conn.execute('INSERT INTO module_Rd4FHNG29WkSgBFEfqe3Kv (hogehoge) VALUES (1), (2), (3)')

#     database = Database(mysql.url)
#     database.register_schemas_and_modules(test_schemas, test_modules)

#     result = database.check_tables()
#     assert len(result.new_tables) == 1
#     assert result.new_tables[0].name == 'meta'
#     assert len(result.alter_tables) == 0
#     assert len(result.error_tables) == 1
#     assert result.error_tables[0].name == 'module_Rd4FHNG29WkSgBFEfqe3Kv'

#     with pytest.raises(MigrationError, message='Excpectiong MigrationError'):
#         database.migrate()


@pytest.mark.usefixtures('mysql')
@pytest.mark.usefixtures('mock_circlecore')
@pytest.mark.asyncio
async def test_store_blob(mysql, mock_circlecore):
    envdir = mock_circlecore[1]

    with MetaDataSession.begin():
        ccinfo = CcInfo.query.filter_by(myself=True).one()

        module = Module.create()
        schema = Schema.create(display_name='Schema', properties='x:int,y:float,data:blob')
        box = MessageBox(uuid=generate_uuid(model=MessageBox), schema=schema, module=module, display_name='Box')

        MetaDataSession.add(schema)
        MetaDataSession.add(module)
        MetaDataSession.add(box)

    database = Database(mysql.url, time_db_dir=envdir, log_dir=envdir)
    connection = database._engine.connect()

    with database._engine.begin() as connection:
        database.store_message(
            box,
            ModuleMessage(
                box.uuid,
                '1545895047.000',
                0,
                {
                    'x': 0,
                    'y': 3.14,
                    'data': BlobMetadata(ccinfo.uuid, 'text/plain', 'deadbeafdeadbeafdeadbeafdeadbeaf')
                },
            ),
            connection=connection
        )

    with database._engine.begin() as connection:
        table = database.find_table_for_message_box(box)
        rows = connection.execute(select([table.c.data])).fetchall()
        print(rows)
        assert len(rows) == 1
        expected = '{{"$data": "deadbeafdeadbeafdeadbeafdeadbeaf", "$source": "{source}", "$type": "text/plain"}}' \
            .format(
                source=str(ccinfo.uuid)
            )
        assert rows[0][0] == expected


@pytest.mark.usefixtures('mysql')
@pytest.mark.usefixtures('mock_circlecore')
@pytest.mark.asyncio
async def test_reconnect(mysql, mock_circlecore):
    envdir = mock_circlecore[1]
    database = Database(mysql.url, time_db_dir=envdir, log_dir=envdir)

    journal_writer = database.make_writer()
    queued_writer = journal_writer.child_writer

    # test reconnect
    await queued_writer.reconnect()
