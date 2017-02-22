# -*- coding: utf-8 -*-

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


class CCWebApp(Flask):
    """Web管理インタフェース用のFlask Application.
    """
    def __init__(self, core, base_url=None):
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

        self.add_url_rule('/replication/<uuid:link_uuid>', endpoint='replication_endpoint', build_only=True)

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

        with self.test_request_context('/'):
            initialize_oauth()

    @property
    def core(self):
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
    """UUID値をURLに使うためのコンバーター.

    :class:`~bson.objectid.ObjectId` objects;
    :attr:`ObjectId`.
    """

    def to_python(self, value):
        try:
            return uuid.UUID(value)
        except ValueError:
            raise abort(404)

    def to_url(self, value):
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
