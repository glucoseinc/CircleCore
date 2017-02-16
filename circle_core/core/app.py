# -*- coding: utf-8 -*-
"""
CircleCoreのCore
"""
import configparser
import contextlib
import logging
import os
import sys
import uuid

import alembic
import alembic.config
import sqlalchemy
import sqlalchemy.exc

from circle_core.exceptions import ConfigError
from circle_core.helpers import Receiver
from circle_core.models import CcInfo, generate_uuid, MetaDataBase, MetaDataSession, NoResultFound
from circle_core.workers import make_worker, WORKER_DATARECEIVER, WORKER_SLAVE_DRIVER
from .base import logger
from .hub import CoreHub
from .metadata_event_logger import MetaDataEventLogger


DFEAULT_CONFIG_FILE_NAME = 'circle_core.ini'


class CircleCore(object):
    @classmethod
    def load_from_config_file(cls, config_filepath):
        """
        コンフィグファイルのパスを指定して読み込む
        """
        config = cls._make_config_parser()
        with open(config_filepath) as fp:
            config.read_file(fp)
        return cls.load_from_config(config)

    @classmethod
    def load_from_default_config_file(cls, debug=False):
        config = cls._make_config_parser()
        okfiles = config.read([
            './{}'.format(DFEAULT_CONFIG_FILE_NAME),
            os.path.expanduser('~/{}'.format(DFEAULT_CONFIG_FILE_NAME)),
            '/etc/circle_core/{}'.format(DFEAULT_CONFIG_FILE_NAME),
        ])
        if not okfiles:
            raise ConfigError('no config file found')

        return cls.load_from_config(config, debug=debug)

    @classmethod
    def _make_config_parser(cls):
        return configparser.ConfigParser(
            delimiters=('=',),
            default_section=None,
            interpolation=configparser.ExtendedInterpolation(),
        )

    @classmethod
    def load_from_config(cls, config, debug=False):
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
        if config_uuid != 'auto':
            try:
                config_uuid = uuid.UUID(config_uuid)
            except ValueError:
                raise ConfigError('invalid uuid `{}`'.fomart(config_uuid))

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
        self.workers.append(make_worker(self, worker_type, worker_key, worker_config))

    def find_worker(self, worker_type, worker_key=None):
        for worker in self.workers:
            if worker.worker_type != worker_type:
                continue

            if worker_key is not None and worker.worker_key != worker_key:
                continue

            return worker

    def run(self):
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
        """Messageを保存している方のデータベース.

        今のとこおｒDatareceiverが握っているのでそれを返す
        CircleCoreが持っているべき???"""
        return self.find_worker(WORKER_DATARECEIVER).db

    def make_hub_receiver(self, topic=None):
        return Receiver(self.hub_socket, topic)

    # private
    def prepare_directories(self):
        """
        """
        def _makedirs_safe(p):
            if not os.path.exists(p):
                os.makedirs(p)

        _makedirs_safe(self.prefix)
        _makedirs_safe(os.path.dirname(self.metadata_file_path))
        _makedirs_safe(os.path.dirname(self.log_file_path))

    def open_log_file(self):
        """ユーザー操作等を記録するためのロガーの設定を行う

        コンソールに出すログの方はcliで初期化する"""
        self.audit_logger = logging.getLogger('circle_core.audit')

    def open_metadata_db(self):
        self.metadata_db_engine = sqlalchemy.create_engine('sqlite:///' + os.path.abspath(self.metadata_file_path))
        MetaDataSession.configure(bind=self.metadata_db_engine)

    def migrate_metadata_db(self):
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
        """metadata dbを対象にalembicの環境を開く"""
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
        """自分のCC Infoを作成する

        :param str config_uuid: uuid, autoの場合は生成する
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
        self.metadata_event_logger = MetaDataEventLogger(self, self.log_file_path)
