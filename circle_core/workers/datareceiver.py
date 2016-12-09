# -*- coding: utf-8 -*-
"""センサデータを受け取って保存する"""

# system module
import logging
import time
from uuid import UUID

from six import PY3

# project module
from circle_core.logger import get_stream_legger
from ..database import Database
from ..exceptions import DatabaseMismatchError, ModuleNotFoundError, SchemaNotFoundError
from ..helpers.nanomsg import Receiver
from ..helpers.topics import SensorDataTopic
from ..models import Metadata

if PY3:
    from typing import Any, Dict


logger = get_stream_legger(__name__)


def run(metadata):
    """clickから起動される.

    とりあえず現時点ではパケット毎にcommitする
    将来的には時間 or パケット数でcommitするようにしたい
    """
    # TODO: Temoprary
    metadata.data_receiver_cycle_time = 10 * 1000
    metadata.data_receiver_cycle_count = 10

    topic = SensorDataTopic()
    receiver = Receiver()
    receiver.set_timeout(metadata.data_receiver_cycle_time)

    db = Database(metadata.database_url)
    db.register_schemas_and_modules(metadata.schemas, metadata.modules)

    if not db.check_tables().is_ok:
        raise

    app = CRCRApp(metadata)
    conn = db._engine.connect()

    trans = conn.begin()
    last_commit_count = 0

    time_before = 0
    counter = 0

    while True:
        try:
            for module_uuid, payload in receiver.incoming_messages(topic):
                if not isinstance(payload, list):
                    payload = [payload]
                logger.debug('received a sensor data for %s : %r', module_uuid, payload)

                try:
                    module, schema = app.find_module_and_schema(module_uuid)
                    table = db.find_table_for_module(module)

                    now = time.time()
                    if time_before != now:
                        counter = 0

                    for packet in payload:
                        # TODO: packetチェック
                        conn.execute(table.insert().values(_counter=counter, **packet))
                        counter += 1
                except:
                    import traceback
                    traceback.print_exc()
                    pass

                last_commit_count += len(payload)
                if last_commit_count >= metadata.data_receiver_cycle_count:
                    break
        except:
            trans.rollback()
            raise
        else:
            # commit
            logger.debug('commit data count=%d', last_commit_count)
            if last_commit_count:
                trans.commit()

                # restart new transaction
                logger.debug('begin new transaction')
                trans = conn.begin()
                last_commit_count = 0


class CRCRApp(object):
    """
    CircleCoreの情報をやりとりするクラス。metadata直接さわるのはアレなので。

    とりあえずここに殴り書きしたけど、ちゃんと纏める
    """
    def __init__(self, metadata):
        """
        @constructor

        :param Metadata metadata: metadata
        """
        self.__metadata = metadata
        self.__modules_cache = {}
        self.__schemas_cache = {}

    def find_module_and_schema(self, module_uuid):
        """
        moduleのUUIDからmoduleとそのschemaを返す

        :param UUID module_uuid: moduleのUUID
        :return Tuple[Module, Schema]: moduleとschema
        """

        assert isinstance(module_uuid, UUID)
        if module_uuid not in self.__modules_cache:
            module = self.__metadata.find_module(module_uuid)
            self.__modules_cache[module_uuid] = module
        module = self.__modules_cache[module_uuid]
        if not module:
            ModuleNotFoundError

        if module.schema_uuid not in self.__schemas_cache:
            schema = self.__metadata.find_schema(module.schema_uuid)
            self.__schemas_cache[module.schema_uuid] = schema
        schema = self.__schemas_cache[module.schema_uuid]
        if not schema:
            raise SchemaNotFoundError

        return module, schema
