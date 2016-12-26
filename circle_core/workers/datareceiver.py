# -*- coding: utf-8 -*-
"""センサデータを受け取って保存する"""

# system module
from datetime import datetime
import time
from uuid import UUID

from six import PY3

# project module
from circle_core.logger import get_stream_logger
from ..database import Database
from ..exceptions import ModuleNotFoundError, SchemaNotFoundError
from ..helpers.nanomsg import Receiver
from ..helpers.topics import SensorDataTopic
from ..models.metadata import MetadataIniFile, MetadataRedis

if PY3:
    from typing import Tuple, Union


logger = get_stream_logger(__name__)


def run(metadata):
    """clickから起動される.

    とりあえず現時点ではパケット毎にcommitする
    将来的には時間 or パケット数でcommitするようにしたい
    """
    # TODO: Temporary
    metadata.data_receiver_cycle_time = 10 * 1000
    metadata.data_receiver_cycle_count = 10

    receiver = Receiver(SensorDataTopic())
    receiver.set_timeout(metadata.data_receiver_cycle_time)

    db = Database(metadata.database_url)
    db.register_message_boxes(metadata.message_boxes, metadata.schemas)

    if not db.check_tables().is_ok:
        # TODO: 例外処理
        raise Exception

    conn = db._engine.connect()

    trans = conn.begin()
    last_commit_count = 0

    while True:
        try:
            for msg in receiver.incoming_messages():
                logger.debug('received a sensor data for %s : %r', msg.module.uuid, msg.payload)

                try:
                    table = db.find_table_for_module(msg.module)
                    query = table.insert().values(
                        _created_at=msg.timestamp,
                        _counter=msg.count,
                        **msg.payload
                    )
                    conn.execute(query)
                except:
                    import traceback
                    traceback.print_exc()
                    pass

                last_commit_count += 1
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
