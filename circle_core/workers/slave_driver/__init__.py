# -*- coding: utf-8 -*-
"""Master側のWebsocketの口とか、AdminのUIとか"""
import logging

import six

# project module
from circle_core.core.metadata_event_listener import MetaDataEventListener
from circle_core.models import ReplicationMaster
from .replicator import Replicator
from ..base import CircleWorker, register_worker_factory

WORKER_SLAVE_DRIVER = 'slave_driver'
logger = logging.getLogger(__name__)


@register_worker_factory(WORKER_SLAVE_DRIVER)
def create_slave_driver(core, type, key, config):
    assert type == WORKER_SLAVE_DRIVER

    return SlaveDriverWorker(
        core, key,
    )


class SlaveDriverWorker(CircleWorker):
    """
    """
    worker_type = WORKER_SLAVE_DRIVER

    def __init__(self, core, worker_key):
        super(SlaveDriverWorker, self).__init__(core, worker_key)

        self.replicators = {}

    def initialize(self):
        for master in ReplicationMaster.query:
            self.start_replicator(master)

        # replicationmasterに関するイベントを監視する
        self.listener = MetaDataEventListener()
        self.listener.on('replicationmaster', 'after', self.on_change_replication_master)

    def run(self):
        pass

    def finalize(self):
        for replicator in six.itervalues(self.replicators):
            replicator.close()

    def start_replicator(self, master):
        replicator = Replicator(self, master)
        self.replicators[master.id] = replicator
        replicator.run()

    def stop_replicator(self, master):
        replicator = self.replicators.pop(master.id)
        if replicator:
            logger.info('close replicator %r for %s', replicator, master.endpoint_url)
            replicator.close()

    def on_change_replication_master(self, what, target):
        assert isinstance(target, ReplicationMaster)

        if what == 'after_delete':
            # 削除されたので、Replicatorを閉じる
            self.stop_replicator(target)
        elif what == 'after_insert':
            # 追加されたので、Replicatorを開く
            self.start_replicator(target)
