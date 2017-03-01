#!/usr/bin/env bash
pip install -e git://github.com/nanomsg/nnpy.git#egg=nnpy
pip install -e git://github.com/graphite-project/whisper.git@b783ab3f577f3f60db607adda241e29b7242bcf4#egg=whisper-0.10.0rc1
pip install http://cdn.mysql.com//Downloads/Connector-Python/mysql-connector-python-2.2.1.tar.gz
pip install -e '.[test,mysql]'
