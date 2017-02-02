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

from circle_core.exceptions import ConfigError
from circle_core.models import CcInfo, generate_uuid, MetaDataBase, MetaDataSession, NoResultFound


DFEAULT_CONFIG_FILE_NAME = 'circle_core.ini'
logger = logging.getLogger('circle_core.core')


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
    def load_from_default_config_file(cls):
        config = cls._make_config_parser()
        okfiles = config.read([
            './{}'.format(DFEAULT_CONFIG_FILE_NAME),
            os.path.expanduser('~/{}'.format(DFEAULT_CONFIG_FILE_NAME)),
            '/etc/circle_core/{}'.format(DFEAULT_CONFIG_FILE_NAME),
        ])
        if not okfiles:
            raise ConfigError('no config file found')

        return cls.load_from_config(config)

    @classmethod
    def _make_config_parser(cls):
        return configparser.ConfigParser(
            delimiters=('=',),
            default_section=None,
        )

    @classmethod
    def load_from_config(cls, config):
        core_config = config['circle_core']

        return cls(
            config_uuid=core_config.get('uuid', 'auto'),
            metadata_file_path=core_config['metadata_file_path'],
            log_file_path=core_config['log_file_path'],
        )

        raise NotImplementedError()

    def __init__(self, config_uuid, metadata_file_path, log_file_path):
        if config_uuid != 'auto':
            try:
                config_uuid = uuid.UUID(config_uuid)
            except ValueError:
                raise ConfigError('invalid uuid `{}`'.fomart(config_uuid))

        self.metadata_file_path = metadata_file_path
        self.log_file_path = log_file_path

        # setup
        self.open_log_file()
        self.open_metadata_db()
        self.migrate_metadata_db()

        self.my_cc_info = self.make_own_cc_info(config_uuid)
        logger.info(
            'My CiclelCore\nUUID: %s\nDisplay Name:%s',
            self.my_cc_info.uuid, self.my_cc_info.display_name)

    def open_log_file(self):
        """ユーザー操作等を記録するためのロガーの設定を行う

        コンソールに出すログの方はcliで初期化する"""
        pass

    def open_metadata_db(self):
        self.metadata_db_engine = sqlalchemy.create_engine('sqlite:///' + os.path.abspath(self.metadata_file_path))
        MetaDataSession.configure(bind=self.metadata_db_engine)

    def migrate_metadata_db(self):
        # dbにTableが一個もなかったらcreate allして、revisionをHEADにする
        dummy = sqlalchemy.MetaData()
        dummy.reflect(self.metadata_db_engine)
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

    @contextlib.contextmanager
    def open_alembic(self):
        """metadata dbを対象にalembicの環境を開く"""
        oldwd = os.getcwd()
        os.chdir(os.path.abspath(os.path.join(os.path.dirname(__file__))))

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
