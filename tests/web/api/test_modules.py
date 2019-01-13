from unittest.mock import MagicMock

from tornado.testing import AsyncHTTPTestCase
from tornado.web import Application, FallbackHandler
from tornado.wsgi import WSGIContainer

from circle_core.models import MessageBox, MetaDataSession, Module, Schema, User
from circle_core.testing import mock_circlecore_context
from circle_core.web import create_app


class AdminWebBase(AsyncHTTPTestCase):

    def get_app(self):
        self.flask_app = create_app(self.app_mock, self.get_url('/'))
        return Application(
            [(r'.*', FallbackHandler, {'fallback': WSGIContainer(self.flask_app)})],
            _core=self.app_mock
        )

    def setUp(self):
        self.app_mock = MagicMock()

        self.ctxt = mock_circlecore_context()
        self.ctxt.__enter__()

        super().setUp()

    def tearDown(self):
        self.ctxt.__exit__(None, None, None)

        super().tearDown()


class NiceTestSuite(AdminWebBase):
    def test_moge(self):
        """API認証"""
        with MetaDataSession.begin():
            user = User.create(account='tester', password='tester')
            user.renew_token()
            schema = Schema.create(display_name='Schema', properties='x:int,y:float,data:blob')
            module = Module.create(display_name='Module')
            mbox = MessageBox(
                uuid='4ffab839-cf56-478a-8614-6003a5980857', schema_uuid=schema.uuid, module_uuid=module.uuid
            )
            MetaDataSession.add(user)
            MetaDataSession.add(schema)
            MetaDataSession.add(module)
            MetaDataSession.add(mbox)

        data_api_endpoint = self.get_url('/api/modules/{}/{}/data'.format(module.uuid, mbox.uuid))

        # 認証がいるよ
        response = self.fetch(data_api_endpoint)
        assert response.code == 403

        # 認証がいるよ
        response = self.fetch(data_api_endpoint, headers={
            'Authorization': 'Bearer {}'.format(user.encoded_token)
        })
        assert response.code == 200
