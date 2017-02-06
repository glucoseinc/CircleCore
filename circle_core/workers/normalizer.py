# -*- coding: utf-8 -*-
"""センサモジュールから突っ込まれるrawなmessageを正規化して戻す"""

# system module
import logging
# from datetime import datetime
import time
# from uuid import UUID
import os

# # project module
# from ..database import Database
# from ..exceptions import ModuleNotFoundError, SchemaNotFoundError
from ..helpers.nanomsg import Receiver, Sender, MasterSender
from ..helpers.topics import ModuleMessageTopic
# from ..helpers.topics import ModuleMessageTopic
# from ..timed_db import TimedDBBundle
# from ..models import Schema, MessageBox
from .base import CircleWorker, register_worker_factory


logger = logging.getLogger(__name__)
WORKER_NORMALIZER = 'normalizer'


import nnpy


class ReqServer(object):
    def __init__(self):
        self._socket = nnpy.Socket(nnpy.AF_SP, nnpy.REP)


class NormalizerWorker(CircleWorker):
    @classmethod
    def create(cls, core, type, key, config):
        assert type == WORKER_NORMALIZER
        return cls(
            core,
            hub=config.get('hub'),
        )

    def __init__(self, core, hub):
        super(NormalizerWorker, self).__init__(core)

        self.hub = hub
        # self.message_receiver = Receiver(hub)
        # self.message_sender = Sender(hub)

    def run(self):
        logger.info('Normalizer running...: %s', os.getpid())

        self.message_sender = MasterSender(self.hub)

        self.server = ReqServer()
        self.server._socket.setsockopt(nnpy.SOL_SOCKET, nnpy.RCVTIMEO, 10000)
        self.server._socket.bind('tcp://127.0.0.1:7890')

        # print('normalizer connect ', self.hub)
        loop = 0
        while True:
            loop += 1
            try:
                # time.sleep(1)
                # continue
                msg = self.server._socket.recv()
            except nnpy.NNError as exc:
                print('{:04d} exc'.format(loop), exc)
                continue

            print('!!', msg)

            self.server._socket.send('ok'.encode('utf-8'))
            self.message_sender._socket.send(msg)

            # print(
            #     ' STAT_ESTABLISHED_CONNECTIONS',
            #     self.message_sender._socket.get_statistic(nnpy.STAT_ESTABLISHED_CONNECTIONS))
            # print(
            #     ' STAT_ACCEPTED_CONNECTIONS',
            #     self.message_sender._socket.get_statistic(nnpy.STAT_ACCEPTED_CONNECTIONS))
            # print(
            #     ' STAT_DROPPED_CONNECTIONS',
            #     self.message_sender._socket.get_statistic(nnpy.STAT_DROPPED_CONNECTIONS))
            # print(
            #     ' STAT_CONNECT_ERRORS',
            #     self.message_sender._socket.get_statistic(nnpy.STAT_CONNECT_ERRORS))
            # print(
            #     ' STAT_CURRENT_CONNECTIONS',
            #     self.message_sender._socket.get_statistic(nnpy.STAT_CURRENT_CONNECTIONS))
            # print(
            #     ' STAT_INPROGRESS_CONNECTIONS',
            #     self.message_sender._socket.get_statistic(nnpy.STAT_INPROGRESS_CONNECTIONS))
            # print(
            #     ' STAT_BYTES_SENT',
            #     self.message_sender._socket.get_statistic(nnpy.STAT_BYTES_SENT))
            # print(
            #     ' STAT_MESSAGES_SENT',
            #     self.message_sender._socket.get_statistic(nnpy.STAT_MESSAGES_SENT))

            # r = self.message_sender.send({'type': 'info', 'payload': {'msg': 'hello normalizer'}})
            # print('send hello', r)
            # time.sleep(1)

        while True:
            for msg in self.message_receiver:
                logger.debug('received a module data for %s-%s : %r', msg.module_uuid, msg.box_id, msg.payload)


register_worker_factory(
    WORKER_NORMALIZER,
    NormalizerWorker.create,
)
