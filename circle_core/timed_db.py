# -*- coding: utf-8 -*-

"""メッセージ数などを記録する時間別DBを管理する."""
from collections import defaultdict
import logging
import os
import threading
from typing import Dict

import whisper


logger = logging.getLogger(__name__)

WHISPER_ARCHIVES_STRING = '1s:24h 10s:7d 10m:150d 1h:3y'.split(' ')
WHISPER_ARCHIVES = [whisper.parseRetentionDef(d) for d in WHISPER_ARCHIVES_STRING]


WHISPER_GLOBAL_LOCK = threading.Lock()
WHISPER_GLOBAL_LOCKS: Dict[str, threading.Lock] = {}


def get_lock(filepath):
    with WHISPER_GLOBAL_LOCK:
        if filepath not in WHISPER_GLOBAL_LOCKS:
            WHISPER_GLOBAL_LOCKS[filepath] = threading.Lock()
        return WHISPER_GLOBAL_LOCKS[filepath]


class TimedDBBundle(object):
    """
    TimedDBをとりまとめるクラス
    """
    def __init__(self, dir_prefix):
        self.dir_prefix = dir_prefix

    def update(self, updates):
        """
        whisperをまとめて更新する
        """

        # updatesをbox_id別に管理する
        sorted_updates = defaultdict(lambda: defaultdict(int))

        # whisperのtimestampは秒単位なので、秒以下はまとめる
        for box_id, timestamp in updates:
            sorted_updates[box_id][int(timestamp)] += 1

        for box_id, timestamps in sorted_updates.items():
            # whisperの中でSORTかけてた
            # timestamps = sorted(timestamps.items())
            timestamps = timestamps.items()

            db_path = os.path.join(self.dir_prefix, TimedDB.make_db_name(box_id))

            if not os.path.exists(db_path):
                logger.debug('create whsiper db for box %s at path %s', box_id, db_path)
                whisper.create(
                    db_path, WHISPER_ARCHIVES,
                    xFilesFactor=0.5,
                    aggregationMethod='sum', sparse=False, useFallocate=True)

            logger.debug('update timed db (%s): %r', box_id, timestamps)
            with get_lock(db_path):
                whisper.update_many(
                    db_path, timestamps
                )

    def find_db(self, box_id):
        return TimedDB(os.path.join(self.dir_prefix, TimedDB.make_db_name(box_id)))


class TimedDB(object):
    """
    1s:24h 10s:7d 10m:150d 1h:3y
    > [(1, 86400), (10, 60480), (600, 21600), (3600, 26280)]

    Archive 0: 86400 points of 1s precision
    Archive 1: 60480 points of 10s precision
    Archive 2: 21600 points of 600s precision
    Archive 3: 26280 points of 3600s precision

    Estimated Whisper DB Size: 2.229MB (2338816 bytes on disk with 4k block

    Estimated storage requirement for 1k metrics: 2.178GB
    Estimated storage requirement for 5k metrics: 10.891GB
    Estimated storage requirement for 10k metrics: 21.782GB
    Estimated storage requirement for 50k metrics: 108.910GB
    Estimated storage requirement for 100k metrics: 217.819GB
    Estimated storage requirement for 500k metrics: 1089.096GB
    """
    @classmethod
    def make_db_name(cls, box_id):
        return 'box_{}.wsp'.format(box_id)

    def __init__(self, filepath):
        self.filepath = filepath

    def fetch(self, start_time, end_time):
        try:
            with get_lock(self.filepath):
                data = whisper.fetch(self.filepath, start_time, end_time)
        except FileNotFoundError:
            return None

        if not data:
            return None

        (start, end, step), values = data

        return start, end, step, values
