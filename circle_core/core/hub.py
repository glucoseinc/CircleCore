# -*- coding: utf-8 -*-
"""
nanomsgのhub
"""

import os

from tornado.ioloop import IOLoop

from .base import logger
from ..helpers.nanomsg import Replier, Sender


class HubError(Exception):
    pass


class InvalidRequestError(HubError):
    pass


class CoreHub(object):
    """nanomsgのpubsubなどを管理するHub

    request_socketでリクエストを待ち受けて、hub_socketのpubsubに流す
    """
    def __init__(self, hub_socket, request_socket):
        self.message_handlers = {}
        self.hub_socket = hub_socket
        self.request_socket = request_socket

    def run(self):
        self.sender = Sender(self.hub_socket)
        self.replier = Replier(self.request_socket)
        self.replier.register_ioloop(self.handle_replier)

        logger.info('Hub running at PID:%s', os.getpid())
        IOLoop.current().start()

    def register_handler(self, name, handler):
        logger.info('register message handler: %s', name)
        self.message_handlers[name] = handler

    def publish(self, topic, message):
        """(topic, message)をpubsubに投げる"""
        self.sender.send(topic, message)

    # private
    def handle_replier(self, request, exception):
        if exception:
            self.replier.send({'response': 'failed', 'message': str(exception)})
            return

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

    def handle_request(self, request):
        reqtype = request['request']

        if reqtype not in self.message_handlers:
            raise InvalidRequestError('Invalid request `{}`'.format(reqtype))

        handler = self.message_handlers[reqtype]
        response = handler(request)
        return response
