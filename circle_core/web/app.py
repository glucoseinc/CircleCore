# -*- coding: utf-8 -*-

"""WebUI."""

# system module
from datetime import datetime
import os
import time
import urllib.parse
import uuid

# community module
from flask import abort, Flask, redirect, render_template, request, url_for
from werkzeug.routing import BaseConverter

# project module
from circle_core.utils import portable_popen
from .authorize.core import oauth


# type annotation
try:
    from typing import TYPE_CHECKING, Union
    if TYPE_CHECKING:
        from circle_core.core import CircleCore
except ImportError:
    pass


class CCWebApp(Flask):
    """Web管理インタフェース用のFlask Application.

    :param float uptime: 起動時刻
    :param int ws_port: Websocket Port Number
    """
    def __init__(self, core, base_url=None, ws_port=None, is_https=False):
        """init.

        :param CircleCore core: CircleCore Core
        :param str base_url: ベースURL
        :param int ws_port: Websocket Port Number
        """
        super(CCWebApp, self).__init__(__name__)

        self.uptime = time.time()
        self.config['SECRET_KEY'] = (
            '16f4ecd3a212450c3bbc22f61c2fa4ea06c5ae7fa8827887e14b469ab59d69d6'
            '574302c7680310a50a5dc70db38d584ace529f0162ec56103cbce6a4c670e417'
        )
        self.config['CORE'] = core
        if core.debug:
            self.config['TEMPLATES_AUTO_RELOAD'] = True

        if base_url:
            t = urllib.parse.urlparse(base_url, scheme='http')
            self.config['PREFERRED_URL_SCHEME'] = t.scheme
            self.config['SERVER_NAME'] = t.netloc
            self.config['APPLICATION_ROOT'] = t.path

            # flaskのデフォルト実装だと、port番号を無視するが、Chromeの最新版(55)は無いとCookieを保存してくれない...
            if ':' in t.netloc and t.netloc.split(':')[1] != {'https': '443', 'http': '80'}[t.scheme]:
                self.config['SESSION_COOKIE_DOMAIN'] = t.netloc
        if is_https:
            self.config['PREFERRED_URL_SCHEME'] = 'https'

        self.url_map.converters['uuid'] = UUIDConverter

        from .api import api
        self.register_blueprint(api, url_prefix='/api')
        from .download import download
        self.register_blueprint(download, url_prefix='/download')
        from .authorize import authorize, oauth
        self.register_blueprint(authorize)
        oauth.init_app(self)
        from .public import public
        self.register_blueprint(public)

        self.ws_port = ws_port

        # favicon
        @self.route('/favicon.ico')
        def favicon_ico():
            return redirect(url_for('static', filename='favicon.ico'))

        @self.route('/', defaults={'path': ''})
        @self.route('/<path:path>')
        def _index(path):
            """WUI root.
            必ず最後に追加すること
            """
            # ここにAPIのリクエストが来たら、それはPathを間違えている
            if request.path.startswith('/api/'):
                raise abort(404)
            return render_template('index.html')

        @self.context_processor
        def global_variables():
            return dict(UPTIME=self.uptime)

        from .authorize.core import initialize_oauth

        # with self.test_request_context('/'):
        with self.app_context():
            initialize_oauth()

    @property
    def core(self):
        """CircleCore Coreを取得する.

        :return: CircleCore Core
        :rtype: CircleCore
        """
        return self.config['CORE']

    def build_frontend(self):
        """WebUI用のフロントエンドのjs, cssをビルドする."""
        import circle_core
        basedir = os.path.abspath(
            os.path.join(
                os.path.dirname(circle_core.__file__),
                os.pardir))

        portable_popen(['npm', 'install', '.'], cwd=basedir).wait()
        portable_popen(['npm', 'run', 'build'], cwd=basedir).wait()


class UUIDConverter(BaseConverter):
    """UUID値をURLに使うためのコンバータ."""

    def to_python(self, value):
        """Pythonで使用できる型に変換する.

        :param str value: UUID
        :return: UUID
        :rtype: uuid.UUID
        """
        try:
            return uuid.UUID(value)
        except ValueError:
            raise abort(404)

    def to_url(self, value):
        """URLで使用できる型に変換する.

        :param Union[str, uuid.UUID] value: UUID
        :return: UUID
        :rtype: str
        """
        return str(value)


def check_login():
    """ログイン確認."""
    t, oauth_requets = oauth.verify_request([])
    user = oauth_requets.user

    if not user:
        raise abort(403)

    # update user's last access
    from circle_core.models import MetaDataSession

    with MetaDataSession.begin():
        user.last_access_at = datetime.utcnow()
        MetaDataSession.add(user)
