# -*- coding: utf-8 -*-
"""モジュールへのイベント受け口
"""
import json
import logging
from email.parser import BytesFeedParser
from typing import TYPE_CHECKING

from tornado.websocket import WebSocketHandler

from circle_core.constants import CRDataType, WebsocketStatusCode
from circle_core.exceptions import InconsitencyError
from circle_core.models import MessageBox, NoResultFound, User

if TYPE_CHECKING:
    from typing import Optional

logger = logging.getLogger(__name__)


class ModuleEventHandler(WebSocketHandler):
    """モジュールへのイベントを受け取る

    """
    mbox: 'Optional[MessageBox]'

    # override
    async def get(self, *args, **kwargs):
        if not self.check_authorize():
            return

        return super().get(*args, **kwargs)

    async def post(self, module_uuid, mbox_uuid):
        if not self.check_authorize():
            return

        self.set_header('Content-Type', 'application/json; charset=UTF-8')

        logger.debug('Post to module %s/%s', module_uuid, mbox_uuid)
        try:
            self.setup(module_uuid, mbox_uuid)
        except NoResultFound:
            self.send_error(404)
            # self.write('Messagebox {}/{} not found'.format(module_uuid, mbox_uuid))
            return

        content_type = self.request.headers.get('Content-Type', '').lower()
        if ';' in content_type:
            content_type = content_type.split(';')[0].strip()

        attachments = {}
        if content_type == 'application/json':
            payload = json.loads(self.request.body.decode('utf-8'))
        elif content_type == 'multipart/mixed':
            parser = BytesFeedParser()
            for k, v in self.request.headers.items():
                parser.feed('{}: {}\n'.format(k, v).encode('utf-8'))
            parser.feed(b'\n')
            parser.feed(self.request.body)
            msg = parser.close()

            if not msg.is_multipart():
                logger.error('Bad multipart request')
                self.send_error(400)
                return

            main_part = msg.get_payload(0)
            if main_part.get_content_type() != 'application/json':
                logger.error('Mainpart is not JSON')
                self.send_error(400)
                return

            payload = json.loads(main_part.get_payload(decode=True))

            for idx in range(1, len(msg.get_payload())):
                part = msg.get_payload(idx)
                if part.is_multipart():
                    logger.error('Nesting multipart is not supported')
                    self.send_error(400)
                    return

                attachments[part.get_filename()] = part.get_content_type(), part.get_payload(decode=True)
        else:
            # Unsupported mimetype
            logger.error('Unsupported content type %s', content_type)
            self.send_error(400)
            return

        # blob プロパティあったらゴニョゴニョする
        blobstore = self.get_core().get_blobstore()
        for prop in self.mbox.schema.properties:
            if prop.type_val != CRDataType.BLOB:
                continue
            data = payload.get(prop.name)

            if data is None:
                pass
            elif data.startswith('data:'):
                payload[prop.name] = blobstore.store_blob_url(self.mbox.uuid, data)
            elif data.startswith('file:///'):
                content_type, data = attachments[data[8:]]
                payload[prop.name] = blobstore.store_blob(self.mbox.uuid, content_type, data)
            else:
                # Unsupported data type
                self.send_error(400)
                return

        datareceiver = self.get_core().get_datareceiver()
        rv = await datareceiver.receive_new_message(str(self.mbox.uuid), payload)

        self.write(json.dumps({'ok': rv}))

    def open(self, module_uuid, mbox_uuid):
        """他のCircleCoreから接続された際に呼ばれる."""
        logger.debug('Connect to module %s/%s', module_uuid, mbox_uuid)
        try:
            self.setup(module_uuid, mbox_uuid)
        except NoResultFound:
            logger.warning('Messagebox %s/%s was not found. Connection close.', module_uuid, mbox_uuid)
            self.close(
                code=WebsocketStatusCode.NOT_FOUND.value,
                reason='Messagebox {}/{} was not found.'.format(module_uuid, mbox_uuid)
            )
            return

        self.datareceiver = self.get_core().get_datareceiver()

    async def on_message(self, plain_msg: str) -> None:
        """WebSocket経由でセンサからメッセージが送られてきた際に呼ばれる.

        {command: command from slave, ...payload}

        :param unicode plain_msg:
        """
        mbox = self.mbox
        if mbox is None:
            raise InconsitencyError

        logger.debug('message received: `%s`' % plain_msg)
        payload = json.loads(plain_msg)

        await self.datareceiver.receive_new_message(str(mbox.uuid), payload)
        # TODO: 書き込めていなかったらエラーを返す

    def on_close(self):
        """センサーとの接続が切れた際に呼ばれる."""
        logger.debug('connection closed: %s', self)

    def check_origin(self, origin):
        """CORSチェック."""
        # wsta等テストツールから投げる場合はTrueにしておく
        return True

    # internal
    def get_core(self):
        return self.application.settings['_core']

    def setup(self, module_uuid, mbox_uuid):
        """mboxの存在チェック"""
        self.mbox = MessageBox.query.filter_by(uuid=mbox_uuid, module_uuid=module_uuid).one()

    def check_authorize(self) -> bool:
        """GET, POST時にAuthorizationをチェックする"""
        auth_payload = self.request.headers.get('Authorization')
        if not auth_payload:
            self.set_status(401)
            self.set_header('Content-Type', 'application/json; charset=UTF-8')
            self.set_header('WWW-Authenticate', 'Bearer realm=""')
            self.write(json.dumps({'ok': 'False', 'message': 'Authorization required'}))
            return False

        status, error = 400, 'xxx'
        try:
            auth_scheme, token = auth_payload.strip().split(' ', 1)
        except ValueError:
            status, error = 400, 'invalid_request'
            auth_scheme = token = ''

        if auth_scheme != 'Bearer':
            status, error = 400, 'bad_scheme'
        else:
            user = User.query.filter_by_encoded_token(token)
            if not user:
                status, error = 401, 'invalid_token'

            # TODO(shn) メッセージ書き込みもScopeほしいよね
            status, error = 200, ''

        if status != 200:
            self.set_status(status)
            self.set_header('Content-Type', 'application/json; charset=UTF-8')
            self.set_header('WWW-Authenticate', 'Bearer realm="",error="{error}"'.format(error=error))
            self.write(json.dumps({'ok': 'False', 'message': error}))

        return status == 200
