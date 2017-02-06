# -*- coding: utf-8 -*-
"""
nanomsgのhub
"""

import logging
import os

from ..helpers.nanomsg import Sender, Replier


logger = logging.getLogger(__name__)


class HubError(Exception):
    pass


class InvalidRequestError(HubError):
    pass


class CoreHub(object):
    """nanomsgのpubsubなどを管理するHub

    request_socketでリクエストを待ち受けて、hub_socketのpubsubに流す
    """
    def __init__(self, hub_socket, request_socket):
        self.sender = Sender(hub_socket)
        self.replier = Replier(request_socket)

        self.message_handlers = {}

    def run(self):
        logger.info('Hub running at PID:%s', os.getpid())

        while True:
            request = self.replier.recv()

            # TODO: 上recv中の例外は的確に対処できているのか????
            try:
                response = self.handle_request(request)
            except Exception as exc:
                import traceback
                traceback.print_exc()
                response = {
                    'response': 'failed',
                    'message': str(exc),
                    'original': request
                }

            self.replier.send(response)

    def register_handler(self, name, handler):
        logger.info('register message handler: %s', name)
        self.message_handlers[name] = handler

    def handle_request(self, request):
        reqtype = request['request']

        if reqtype not in self.message_handlers:
            raise InvalidRequestError('Invalid request `{}`'.format(reqtype))

        handler = self.message_handlers[reqtype]
        response = handler(request)
        return response

    def publish(self, topic, message):
        """(topic, message)をpubsubに投げる"""
        self.sender.send(topic, message)
