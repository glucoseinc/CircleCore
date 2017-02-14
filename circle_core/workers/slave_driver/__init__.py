# -*- coding: utf-8 -*-
"""Master側のWebsocketの口とか、AdminのUIとか"""
# project module
from circle_core.models import ReplicationMaster
from .replicator import Replicator
from ..base import CircleWorker, register_worker_factory

WORKER_SLAVE_DRIVER = 'slave_driver'


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

        self.replicators = []

    def initialize(self):
        for master in ReplicationMaster.query:
            self.start_replicator(master)

    def run(self):
        pass

    def finalize(self):
        for replicator in self.replicators:
            replicator.close()

    def start_replicator(self, master):
        replicator = Replicator(self, master)
        self.replicators.append(replicator)
        replicator.run()
