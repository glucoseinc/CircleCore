# -*- coding: utf-8 -*-
"""CircleCoreのCore."""

# system module
import configparser
import contextlib
import logging
import os
import uuid
from typing import Any, Mapping, Optional, TYPE_CHECKING, cast

# community module
import alembic
import alembic.config

import sqlalchemy
import sqlalchemy.exc

# project module
from circle_core.exceptions import ConfigError
from circle_core.helpers import Receiver
from circle_core.models import CcInfo, MetaDataBase, MetaDataSession, NoResultFound, generate_uuid

from .base import logger
from .hub import CoreHub
from .metadata_event_logger import MetaDataEventLogger

# type annotation
if TYPE_CHECKING:
    from typing import List

    from sqlalchemy.engine import Engine
    from ..database import Database
    from ..types import UUIDLike
    from ..workers import BlobStoreWorker, CircleWorker, WorkerKey, WorkerType

DEFAULT_CONFIG_FILE_NAME = 'circle_core.ini'


class CircleCore(object):
    """CircleCore Core Object.

    Attributes:
        debug (bool): Debugフラグ
        prefix (str): crcrのデータを保存するディレクトリ
        metadata_file_path (str): metadataを保存するファイルのパス
        log_file_path (str): metadata変更ログを保存するファイルのパス
        hub_socket (str): nanomsgのメッセージが流通するHubのSocket
        request_socket (str): nanomsgへのリクエストを受け付けるSocket
        hub (CoreHub): nanomsgのpubsubなどを管理するHub
        my_cc_info (circle_core.models.CcInfo): 自身のCircleCore情報
        Logger (logging) audit_logger: ユーザー操作等を記録するためのロガー
        metadata_event_logger (MetaDataEventLogger): metadataイベントのロガー
        metadata_db_engine: metadataデータベースエンジン
        workers: ワーカーリスト

    Args:
        config_uuid (str): 自身のUUID 'auto'の場合は自動生成する
        prefix (str): crcrのデータを保存するディレクトリ
        metadata_file_path (str): metadataを保存するファイルのパス
        log_file_path (str): metadata変更ログを保存するファイルのパス
        hub_socket (str): nanomsgのメッセージが流通するHubのSocket
        request_socket (str): nanomsgへのリクエストを受け付けるSocket
        debug (bool): Debugフラグ
    """
    metadata_db_engine: 'Engine'
    workers: 'List[CircleWorker]'

    @classmethod
    def load_from_config_file(cls, config_filepath, debug=False):
        """コンフィグファイルのパスを指定して読み込む.

        Args:
            config_filepath (str): コンフィグファイルのパス
            debug (bool): Debugフラグ

        Returns:
            circle_core.core.CircleCore: Core Object
        """
        config = cls._make_config_parser()
        with open(config_filepath) as fp:
            config.read_file(fp)
        return cls.load_from_config(config, debug)

    @classmethod
    def load_from_default_config_file(cls, debug=False):
        """デフォルトのコンフィグファイルを読み込む.

        Args:
            debug (bool): Debugフラグ

        Returns:
            circle_core.core.CircleCore: Core Object
        """
        config = cls._make_config_parser()
        okfiles = config.read(
            [
                './{}'.format(DEFAULT_CONFIG_FILE_NAME),
                os.path.expanduser('~/{}'.format(DEFAULT_CONFIG_FILE_NAME)),
                '/etc/circle_core/{}'.format(DEFAULT_CONFIG_FILE_NAME),
            ]
        )
        if not okfiles:
            raise ConfigError('no config file found')

        return cls.load_from_config(config, debug=debug)

    @classmethod
    def _make_config_parser(cls) -> configparser.ConfigParser:
        """ConfigParserを作成する.

        Returns:
            configparser.ConfigParser: ConfigParser
        """
        return configparser.ConfigParser(
            delimiters=('=',),
            default_section=None,
            interpolation=configparser.ExtendedInterpolation(),
        )

    @classmethod
    def load_from_config(cls, config, debug=False):
        """コンフィグを読み込む.

        Args:
            config (configparser.ConfigParser): コンフィグ
            debug (bool): Debugフラグ

        Returns:
            circle_core.core.CircleCore: Core Object
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
        from circle_core.workers import WORKER_DATARECEIVER, WORKER_SLAVE_DRIVER

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
        if config_uuid != 'auto':
            try:
                config_uuid = uuid.UUID(config_uuid)
            except ValueError:
                raise ConfigError('invalid uuid `{}`'.format(config_uuid))

        if not check_nnurl(hub_socket):
            raise ValueError('Bad hub socket url : {}'.format(hub_socket))
        if not check_nnurl(request_socket):
            raise ValueError('Bad request socket url : {}'.format(request_socket))

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
        logger.info('This CiclelCore > UUID:%s Display Name:%s', self.my_cc_info.uuid, self.my_cc_info.display_name)

    # public
    def add_worker(self, worker_type: 'WorkerType', worker_key: 'WorkerKey', worker_config: Mapping[str, Any]) -> None:
        """ワーカーを追加する.

        Args:
            worker_type (str): ワーカーのタイプ
            worker_key (str): ワーカーのキー
            worker_config (configparser.SectionProxy): ワーカーのコンフィグ
        """
        from circle_core.workers import make_worker

        self.workers.append(make_worker(self, worker_type, worker_key, worker_config))

    def find_worker(
        self, worker_type: 'WorkerType', worker_key: 'Optional[WorkerKey]' = None
    ) -> 'Optional[CircleWorker]':
        """合致するワーカーを取得する.

        Args:
            worker_type: ワーカーのタイプ
            worker_key: ワーカーのキー

        Returns:
            合致するワーカー
        """
        for worker in self.workers:
            if worker.worker_type != worker_type:
                continue

            if worker_key is not None and worker.worker_key != worker_key:
                continue

            return worker
        return None

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

    def get_datareceiver(self):
        """DataReceiverを返す

        :return: Messageデータベース
        :rtype: DataReceiver
        """
        from circle_core.workers import WORKER_DATARECEIVER

        return self.find_worker(WORKER_DATARECEIVER)

    def get_database(self) -> 'Database':
        """Messageデータベースを取得する.

        今のところDatareceiverが握っているのでそれを返す

        Returns:
            Messageデータベース
        """
        return cast('Database', self.get_datareceiver().db)

    def get_blobstore(self) -> 'BlobStoreWorker':
        from circle_core.workers import WORKER_BLOBSTORE

        return cast('BlobStoreWorker', self.find_worker(WORKER_BLOBSTORE))

    def make_hub_receiver(self, topic=None):
        """Message Hubのレシーバを作成する.

        Args:
            topic (Optional[str]): topic名

        Returns:
            circle_core.helpers.Receiver: Message Hubのレシーバ
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

    def make_own_cc_info(self, config_uuid: 'UUIDLike') -> CcInfo:
        """自身のCircleCore Infoを作成する.

        Args:
            config_uuid (str): uuid, autoの場合は生成する

        Returns:
            circle_core.models.CcInfo: 自身のCircleCore Info
        """
        with MetaDataSession.begin():
            try:
                my_cc_info = CcInfo.query.filter_by(myself=True).one()
            except NoResultFound:
                logger.info('My CCInfo not found. Create new one')
                my_cc_info = CcInfo(display_name='My CircleCore', myself=True, work='')
                if config_uuid == 'auto':
                    my_cc_info.uuid = generate_uuid(model=CcInfo)
                else:
                    my_cc_info.uuid = config_uuid

                MetaDataSession.add(my_cc_info)

        return my_cc_info

    def start_metadata_event_logger(self):
        """metadataイベントのロガーを設定する."""
        self.metadata_event_logger = MetaDataEventLogger(self, self.log_file_path)


def check_nnurl(sockurl):
    """nanomsgのURLを事前にチェックする"""
    # いまのところipc:/だけ
    if sockurl.startswith('ipc:///'):
        path = sockurl[6:]
        # unix socketのpathはmax 90文字程度らしい
        # http://pubs.opengroup.org/onlinepubs/007904975/basedefs/sys/un.h.html
        if len(path) > 90:
            return False

    return True
