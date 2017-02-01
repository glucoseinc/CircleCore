# -*- coding: utf-8 -*-

import os

test_root = os.path.dirname(os.path.abspath(__file__))
ini_file_name = 'metadata.ini'
ini_file_path = os.path.join(test_root, ini_file_name)
log_ltsv_name = 'log.ltsv'
log_ltsv_path = os.path.join(test_root, log_ltsv_name)
url_scheme_ini_file = 'file://{}'.format(ini_file_path)

crcr_uuid = '0d749b81-9178-4bc8-932e-d09d6a29941e'
