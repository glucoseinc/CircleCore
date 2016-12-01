# -*- coding: utf-8 -*-
"""センサデータを受け取って保存する"""

# system module
from logging import getLogger
import time
from uuid import UUID

from six import PY3

# project module
from ..database import Database
from ..exceptions import DatabaseMismatchError, DeviceNotFoundError, SchemaNotFoundError
from ..helpers.nanomsg import Receiver
from ..helpers.topics import SensorDataTopic

if PY3:
    from typing import Any, Dict


logger = getLogger(__name__)


def run(config):
    """clickから起動される.

    とりあえず現時点ではパケット毎にcommitする
    将来的には時間 or パケット数でcommitするようにしたい
    """
    # TODO: Temoprary
    config.data_receiver_cycle_time = 10 * 1000
    config.data_receiver_cycle_count = 10

    topic = SensorDataTopic()
    receiver = Receiver()
    receiver.set_timeout(config.data_receiver_cycle_time)

    db = Database(config.database_url)
    db.register_schemas_and_devices(config.schemas, config.devices)

    if not db.check_tables().is_ok:
        raise

    app = CRCRApp(config)
    conn = db._engine.connect()

    trans = conn.begin()
    last_commit_count = 0

    time_before = 0
    counter = 0

    while True:
        try:
            for device_uuid, payload in receiver.incoming_messages(topic):
                if not isinstance(payload, list):
                    payload = [payload]
                logger.debug('received a sensor data for %s : %r', device_uuid, payload)

                try:
                    device, schema = app.find_device_and_schema(device_uuid)
                    table = db.find_table_for_device(device)

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
                if last_commit_count >= config.data_receiver_cycle_count:
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
    CircleCoreの情報をやりとりするクラス。config直接さわるのはアレなので。

    とりあえずここに殴り書きしたけど、ちゃんと纏める
    """
    def __init__(self, config):
        """
        @constructor

        :param circle_core.models.config.config_base.Config config: config
        """
        self.__config = config
        self.__devices_cache = {}
        self.__schemas_cache = {}

    def find_device_and_schema(self, device_uuid):
        """
        deviceのUUIDからdeviceとそのschemaを返す

        :param UUID device_uuid: deviceのUUID
        :return Tuple[Device, Schema]: deviceとschema
        """

        assert isinstance(device_uuid, UUID)
        if device_uuid not in self.__devices_cache:
            device = self.__config.find_device(device_uuid)
            self.__devices_cache[device_uuid] = device
        device = self.__devices_cache[device_uuid]
        if not device:
            DeviceNotFoundError

        if device.schema_uuid not in self.__schemas_cache:
            schema = self.__config.find_schema(device.schema_uuid)
            self.__schemas_cache[device.schema_uuid] = schema
        schema = self.__schemas_cache[device.schema_uuid]
        if not schema:
            raise SchemaNotFoundError

        return device, schema
