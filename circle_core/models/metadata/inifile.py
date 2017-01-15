# -*- coding: utf-8 -*-

# system module
import os

# community module
from six import PY3
from six.moves import configparser
from six.moves.urllib.parse import urlparse

# project module
from .base import MetadataError, MetadataReader
from ..invitation import Invitation
from ..message_box import MessageBox
from ..module import Module
from ..schema import Schema
from ..user import User

if PY3:
    from typing import List


class MetadataIniFile(MetadataReader):
    """MetadataIniFileオブジェクト.

    :param str ini_file_path: INIファイルパス
    """

    stringified_type = 'INI File'

    def __init__(self, ini_file_path):
        """init.

        :param str ini_file_path: INIファイルパス
        """
        super(MetadataIniFile, self).__init__()
        self.ini_file_path = ini_file_path

    @classmethod
    def parse_url_scheme(cls, url_scheme):
        """URLスキームからMetadataオブジェクトを生成する.

        :param str url_scheme: URLスキーム
        :return: Metadataオブジェクト
        :rtype: MetadataIniFile
        """
        ini_file_path = urlparse(url_scheme).path
        if not os.path.exists(ini_file_path):
            raise MetadataError('INI file "{}" not found.'.format(ini_file_path))

        return MetadataIniFile(ini_file_path)

    @property
    def invitations(self):
        """全てのInvitationオブジェクト.

        :return: Invitationオブジェクトリスト
        :rtype: List[Invitation]
        """
        parser = configparser.ConfigParser()
        parser.read(self.ini_file_path)

        invitations = []
        for section in parser.sections():
            if not Invitation.is_key_matched(section):
                continue

            d = dict(parser.items(section))
            # iniファイルからの招待リンクは常に無制限招待
            invitations.append(Invitation(d['uuid'], 0, None))
        return invitations

    @property
    def schemas(self):
        """全てのSchemaオブジェクト.

        :return: Schemaオブジェクトリスト
        :rtype: List[Schema]
        """
        parser = configparser.ConfigParser()
        parser.read(self.ini_file_path)
        schema_dicts = [dict(parser.items(section)) for section in parser.sections() if Schema.is_key_matched(section)]
        schemas = []
        for schema_dict in schema_dicts:
            properties_string = schema_dict.pop('properties', None)
            if properties_string is not None:
                schema_dict['dictified_properties'] = Schema.dictify_properties(properties_string)
            schemas.append(Schema(**schema_dict))
        return schemas

    @property
    def message_boxes(self):
        """全てのMessageBoxオブジェクト.

        :return: MessageBoxオブジェクトリスト
        :rtype: List[MessageBox]
        """
        parser = configparser.ConfigParser()
        parser.read(self.ini_file_path)
        message_box_dicts = [dict(parser.items(section)) for section in parser.sections()
                             if MessageBox.is_key_matched(section)]
        return [MessageBox(**message_box_dict) for message_box_dict in message_box_dicts]

    @property
    def modules(self):
        """全てのModuleオブジェクト.

        :return: Moduleオブジェクトリスト
        :rtype: List[Module]
        """
        parser = configparser.ConfigParser()
        parser.read(self.ini_file_path)
        module_dicts = [dict(parser.items(section)) for section in parser.sections() if Module.is_key_matched(section)]
        return [Module(**module_dict) for module_dict in module_dicts]

    @property
    def users(self):
        """全てのUserオブジェクト.

        :return: Userオブジェクトリスト
        :rtype: List[User]
        """
        parser = configparser.ConfigParser()
        parser.read(self.ini_file_path)
        user_dicts = [dict(parser.items(section)) for section in parser.sections()
                      if User.is_key_matched(section)]
        return [User(**user_dict) for user_dict in user_dicts]
