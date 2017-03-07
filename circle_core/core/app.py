# -*- coding: utf-8 -*-

"""CircleCoreのCore."""

# system module
import configparser
import contextlib
import logging
import os
import uuid

# community module
import alembic
import alembic.config
import sqlalchemy
import sqlalchemy.exc

# project module
from circle_core.exceptions import ConfigError
from circle_core.helpers import Receiver
from circle_core.models import CcInfo, generate_uuid, MetaDataBase, MetaDataSession, NoResultFound
from circle_core.workers import make_worker, WORKER_DATARECEIVER, WORKER_SLAVE_DRIVER
from .base import logger
from .hub import CoreHub
from .metadata_event_logger import MetaDataEventLogger


# type annotation
try:
    from typing import List, Optional, TYPE_CHECKING
    if TYPE_CHECKING:
        from sqlalchemy.engine import Engine
        from ..database import Database
except ImportError:
    pass


DEFAULT_CONFIG_FILE_NAME = 'circle_core.ini'


class CircleCore(object):
    """CircleCore Core Object.

    :param bool debug: Debugフラグ
    :param str prefix: crcrのデータを保存するディレクトリ
    :param str metadata_file_path: metadataを保存するファイルのパス
    :param str log_file_path: metadata変更ログを保存するファイルのパス
    :param List workers: ワーカーリスト
    :param str hub_socket: nanomsgのメッセージが流通するHubのSocket
    :param str request_socket: nanomsgへのリクエストを受け付けるSocket
    :param CoreHub hub: nanomsgのpubsubなどを管理するHub
    :param CcInfo my_cc_info: 自身のCircleCore情報
    :param logging.Logger audit_logger: ユーザー操作等を記録するためのロガー
    :param Engine metadata_db_engine: metadataデータベースエンジン
    :param MetaDataEventLogger metadata_event_logger: metadataイベントのロガー
    """

    @classmethod
    def load_from_config_file(cls, config_filepath, debug=False):
        """コンフィグファイルのパスを指定して読み込む.

        :param str config_filepath: コンフィグファイルのパス
        :param bool debug: Debugフラグ
        :return: CircleCore Core Object
        :rtype: CircleCore
        """
        config = cls._make_config_parser()
        with open(config_filepath) as fp:
            config.read_file(fp)
        return cls.load_from_config(config, debug)

    @classmethod
    def load_from_default_config_file(cls, debug=False):
        """デフォルトのコンフィグファイルを読み込む.

        :param bool debug: Debugフラグ
        :return: CircleCore Core Object
        :rtype: CircleCore
        """
        config = cls._make_config_parser()
        okfiles = config.read([
            './{}'.format(DEFAULT_CONFIG_FILE_NAME),
            os.path.expanduser('~/{}'.format(DEFAULT_CONFIG_FILE_NAME)),
            '/etc/circle_core/{}'.format(DEFAULT_CONFIG_FILE_NAME),
        ])
        if not okfiles:
            raise ConfigError('no config file found')

        return cls.load_from_config(config, debug=debug)

    @classmethod
    def _make_config_parser(cls):
        """ConfigParserを作成する.

        :return: ConfigParser
        :rtype: configparser.ConfigParser
        """
        return configparser.ConfigParser(
            delimiters=('=',),
            default_section=None,
            interpolation=configparser.ExtendedInterpolation(),
        )

    @classmethod
    def load_from_config(cls, config, debug=False):
        """コンフィグを読み込む.

        :param configparser.ConfigParser config: コンフィグ
        :param bool debug: Debugフラグ
        :return: CircleCore Core Object
        :rtype: CircleCore
        """
        core_config = config['circle_core']

        core = cls(
            config_uuid=core_config.get('uuid', 'auto'),
            prefix=core_config.get('prefix'),
            metadata_file_path=core_config['metadata_file_path'],
            log_file_path=core_config['log_file_path'],
            hub_socket=core_config['hub_socket'],
            request_socket=core_config['request_socket'],
            debug=debug,
        )

        # add default workers
        core.add_worker(WORKER_DATARECEIVER, '', core_config)
        core.add_worker(WORKER_SLAVE_DRIVER, '', core_config)

        # add workers
        for section in config.sections():
            if not section.startswith('circle_core:'):
                continue

            t = section.split(':')[1:]
            if len(t) == 1:
                worker_type, worker_key = t[0], ''
            elif len(t) == 2:
                worker_type, worker_key = t[:2]
            else:
                continue

            worker_config = config[section]
            core.add_worker(worker_type, worker_key, worker_config)

        return core

    def __init__(self, config_uuid, prefix, metadata_file_path, log_file_path, hub_socket, request_socket, debug=False):
        """init.

        :param str config_uuid: 自身のUUID 'auto'の場合は自動生成する
        :param str prefix: crcrのデータを保存するディレクトリ
        :param str metadata_file_path: metadataを保存するファイルのパス
        :param str log_file_path: metadata変更ログを保存するファイルのパス
        :param str hub_socket: nanomsgのメッセージが流通するHubのSocket
        :param str request_socket: nanomsgへのリクエストを受け付けるSocket
        :param bool debug: Debugフラグ
        """
        if config_uuid != 'auto':
            try:
                config_uuid = uuid.UUID(config_uuid)
            except ValueError:
                raise ConfigError('invalid uuid `{}`'.format(config_uuid))

        self.debug = debug
        self.prefix = prefix
        self.metadata_file_path = metadata_file_path
        self.log_file_path = log_file_path
        self.workers = []
        self.hub_socket = hub_socket
        self.request_socket = request_socket

        self.hub = CoreHub(self.hub_socket, self.request_socket)

        # setup
        self.prepare_directories()
        self.open_log_file()
        self.open_metadata_db()
        self.migrate_metadata_db()
        self.start_metadata_event_logger()

        self.my_cc_info = self.make_own_cc_info(config_uuid)
        logger.info(
            'This CiclelCore > UUID:%s Display Name:%s',
            self.my_cc_info.uuid, self.my_cc_info.display_name)

    # public
    def add_worker(self, worker_type, worker_key, worker_config):
        """ワーカーを追加する.

        :param str worker_type: ワーカーのタイプ
        :param str worker_key: ワーカーのキー
        :param configparser.SectionProxy worker_config: ワーカーのコンフィグ
        """
        self.workers.append(make_worker(self, worker_type, worker_key, worker_config))

    def find_worker(self, worker_type, worker_key=None):
        """合致するワーカーを取得する.

        :param worker_type: ワーカーのタイプ
        :param worker_key: ワーカーのキー
        :return: 合致するワーカー
        :rtype: Optional[Any]
        """
        for worker in self.workers:
            if worker.worker_type != worker_type:
                continue

            if worker_key is not None and worker.worker_key != worker_key:
                continue

            return worker

    def run(self):
        """CircleCoreを起動する."""
        for worker in self.workers:
            worker.initialize()

        if self.debug:
            from tornado import autoreload
            autoreload.start()

        try:
            self.hub.run()
        finally:
            for worker in self.workers:
                worker.finalize()

    def get_database(self):
        """Messageデータベースを取得する.

        今のところDatareceiverが握っているのでそれを返す

        :return: Messageデータベース
        :rtype: Database
        """
        return self.find_worker(WORKER_DATARECEIVER).db

    def make_hub_receiver(self, topic=None):
        """Message Hubのレシーバを作成する.

        :param Optional[str] topic: topic名
        :return: Message Hubのレシーバ
        :rtype: Receiver
        """
        return Receiver(self.hub_socket, topic)

    # private
    def prepare_directories(self):
        """必要なディレクトリを作成する."""
        def _makedirs_safe(p):
            if not os.path.exists(p):
                os.makedirs(p)

        _makedirs_safe(self.prefix)
        _makedirs_safe(os.path.dirname(self.metadata_file_path))
        _makedirs_safe(os.path.dirname(self.log_file_path))

    def open_log_file(self):
        """ユーザー操作等を記録するためのロガーの設定を行う.

        コンソールに出すログの方はcliで初期化する
        """
        self.audit_logger = logging.getLogger('circle_core.audit')

    def open_metadata_db(self):
        """metadataデータベースの設定をする."""
        self.metadata_db_engine = sqlalchemy.create_engine('sqlite:///' + os.path.abspath(self.metadata_file_path))
        MetaDataSession.configure(bind=self.metadata_db_engine)

    def migrate_metadata_db(self):
        """metadataデータベースのマイグレーションを行う."""
        # dbにTableが一個もなかったらcreate allして、revisionをHEADにする
        dummy = sqlalchemy.MetaData()
        try:
            dummy.reflect(self.metadata_db_engine)
        except sqlalchemy.exc.OperationalError:
            pass

        if not dummy.tables:
            # empty
            logger.info('Initialize metadata database.')
            MetaDataBase.metadata.create_all(self.metadata_db_engine)

            with self.open_alembic() as alembic_cfg:
                alembic.command.stamp(alembic_cfg, 'head')

        else:
            logger.info('Migrate metadata database.')

            with self.open_alembic() as alembic_cfg:
                alembic.command.upgrade(alembic_cfg, 'head')

        # DEBUG
        MetaDataBase.metadata.create_all(self.metadata_db_engine)

    @contextlib.contextmanager
    def open_alembic(self):
        """metadataデータベースを対象にalembicの環境を開く."""
        oldwd = os.getcwd()
        os.chdir(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))

        try:
            alembic_cfg = alembic.config.Config(os.path.abspath(os.path.join('alembic', 'alembic.ini')))
            # alembic_cfg.set_main_option('url', str(self.metadata_db_engine.url))
            with self.metadata_db_engine.begin() as connection:
                alembic_cfg.attributes['connection'] = connection
                yield alembic_cfg
        finally:
            os.chdir(oldwd)

    def make_own_cc_info(self, config_uuid):
        """自身のCircleCore Infoを作成する.

        :param str config_uuid: uuid, autoの場合は生成する
        :return: 自身のCircleCore Info
        :rtype: CcInfo
        """
        with MetaDataSession.begin():
            try:
                my_cc_info = CcInfo.query.filter_by(myself=True).one()
                logger.info('My CCInfo found.')
            except NoResultFound:
                logger.info('My CCInfo not found. Create new one')
                my_cc_info = CcInfo(
                    display_name='My CircleCore',
                    myself=True,
                    work=''
                )
                if config_uuid == 'auto':
                    my_cc_info.uuid = generate_uuid(model=CcInfo)
                else:
                    my_cc_info.uuid = config_uuid

                MetaDataSession.add(my_cc_info)

        return my_cc_info

    def start_metadata_event_logger(self):
        """metadataイベントのロガーを設定する."""
        self.metadata_event_logger = MetaDataEventLogger(self, self.log_file_path)
