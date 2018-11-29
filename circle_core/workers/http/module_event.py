# -*- coding: utf-8 -*-
"""モジュールへのイベント受け口
"""
import json
import logging

from tornado import gen
from tornado.websocket import WebSocketHandler

from circle_core.constants import WebsocketStatusCode
from circle_core.models import MessageBox, NoResultFound


logger = logging.getLogger(__name__)


class ModuleEventHandler(WebSocketHandler):
    """モジュールへのイベントを受け取る

    :param UUID mbox_uuid:
    """

    def open(self, module_uuid, mbox_uuid):
        """他のCircleCoreから接続された際に呼ばれる."""
        logger.debug('Connect to module %s/%s', module_uuid, mbox_uuid)
        self.module_uuid = module_uuid
        self.mbox_uuid = mbox_uuid

        try:
            mbox = MessageBox.query.filter_by(uuid=mbox_uuid, module_uuid=module_uuid).one()
        except NoResultFound:
            logger.warning('Messagebox %s/%s was not found. Connection close.', module_uuid, mbox_uuid)
            self.close(code=WebsocketStatusCode.NOT_FOUND.value,
                       reason='Messagebox {}/{} was not found.'.format(module_uuid, mbox_uuid))
            return
        else:
            self.mbox_uuid = mbox.uuid
            self.module_uuid = mbox.module_uuid

        self.datareceiver = self.get_core().get_datareceiver()

    def get_core(self):
        return self.application.settings['_core']

    @gen.coroutine
    def on_message(self, plain_msg):
        """センサーからメッセージが送られてきた際に呼ばれる.

        {command: command from slave, ...payload}

        :param unicode plain_msg:
        """
        logger.debug('message received: `%s`' % plain_msg)
        payload = json.loads(plain_msg)

        print('!?', self.datareceiver.receive_new_message)
        self.datareceiver.receive_new_message(str(self.mbox_uuid), payload)

    def on_close(self):
        """センサーとの接続が切れた際に呼ばれる."""
        logger.debug('connection closed: %s', self)

    def check_origin(self, origin):
        """CORSチェック."""
        # wsta等テストツールから投げる場合はTrueにしておく
        return True
