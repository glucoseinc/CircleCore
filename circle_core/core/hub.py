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
        self.hub = Sender(hub_socket)
        self.replier = Replier(request_socket)

    def run(self):
        logger.info('Hub running at PID:%s', os.getpid())

        while True:
            request = self.replier.recv()

            # TODO: 上recv中の例外は的確に対処できているのか????
            try:
                # テスト
                self.hub.send('echo', request)

                response = self.handle_request(request)
            except Exception as exc:
                response = {
                    'response': 'failed',
                    'message': str(exc),
                    'original': request
                }

            self.replier.send(response)

    def handle_request(self, request):
        reqtype = request['request']

        raise InvalidRequestError(reqtype)
