# -*- coding: utf-8 -*-

"""メッセージ数などを記録する時間別DBを管理する."""
from collections import defaultdict
import os

import whisper

from circle_core.logger import get_stream_logger


logger = get_stream_logger(__name__)

WHISPER_ARCHIVES_STRING = '1s:24h 10s:7d 10m:150d 1h:3y'.split(' ')
WHISPER_ARCHIVES = [whisper.parseRetentionDef(d) for d in WHISPER_ARCHIVES_STRING]


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
            whisper.update_many(
                db_path, timestamps
            )


class TimedDB(object):
    """

    検討:
    表示区間                      Datapoint数
    30m   1800s                 360  5s
    1h    60m    3600s          360  10s   x2
    6h    360m   21600s         360  1m    x6
    1d    24h    1440m          360  4m    x4
    7d    168h   10080m         336  30m   x7.5
    1m    30d    1800h          450  4h    x8
    1y    12m    365d    8760h  730  12h   x3

    とりあえず以下の時系列で
    5s:2h 1m:24h 5m:7d 30m:30d
    """
    pass

    @classmethod
    def make_db_name(cls, box_id):
        return 'box_{}.wsp'.format(box_id)
