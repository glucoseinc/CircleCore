# -*- coding: utf-8 -*-
import contextlib
import os
import re
import tempfile

import sqlalchemy
from sqlalchemy.pool import NullPool

from circle_core.models import CcInfo, MetaDataBase, MetaDataSession, generate_uuid

temp_db_path = None


@contextlib.contextmanager
def mock_circlecore_context():
    with tempfile.TemporaryDirectory('cc_') as tmp_dir:
        assert os.path.exists(tmp_dir)
        assert not os.path.exists(os.path.join(tmp_dir, 'metadata.sqlite3'))
        metadata_db_engine = sqlalchemy.create_engine(
            'sqlite:///' + os.path.join(tmp_dir, 'metadata.sqlite3'), poolclass=NullPool
        )
        MetaDataSession.configure(bind=metadata_db_engine)
        # empty
        MetaDataBase.metadata.create_all(metadata_db_engine)

        # make my CcInfo
        with MetaDataSession.begin():
            my_cc_info = CcInfo(display_name='My CircleCore', myself=True, work='')
            my_cc_info.uuid = generate_uuid(model=CcInfo)
            MetaDataSession.add(my_cc_info)

        yield metadata_db_engine, tmp_dir

        MetaDataBase.metadata.drop_all(metadata_db_engine)
        MetaDataSession.remove()


test_root = os.path.dirname(os.path.abspath(__file__))
# ini_file_name = 'metadata.ini'
# ini_file_path = os.path.join(test_root, ini_file_name)
# log_ltsv_name = 'log.ltsv'
# log_ltsv_path = os.path.join(test_root, log_ltsv_name)
# url_scheme_ini_file = 'file://{}'.format(ini_file_path)

crcr_uuid = '0d749b81-9178-4bc8-932e-d09d6a29941e'

uuid_rex = re.compile('([0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12})')
