# -*- coding: utf-8 -*-

import os

test_root = os.path.dirname(os.path.abspath(__file__))
ini_file_path = os.path.join(test_root, 'config.ini')
log_ltsv_path = os.path.join(test_root, 'log.ltsv')
url_scheme_ini_file = 'file://{}'.format(ini_file_path)
