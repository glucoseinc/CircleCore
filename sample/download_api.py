#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
ダウンロードAPIサンプル.

curlコマンドを使用する場合
  curl -u <username>:<password> <base uri>/download/<module uuid>/<box uuid>/?start=<YYYYMMDD>\&end=<YYYYMMDD> -o <filename>
start, end, -oオプションは省略可。

Example
  curl -u admin:admin_password http://127.0.0.1:8080/download/467ba25c-1106-4f0a-8e90-cbcc20e5a61d/7194b869-9aeb-4c02-8f84-a041c3c224b9/?start=20170303\&end=20170303 -o download.csv
"""

import urllib.request
from uuid import UUID

import click


def setup_basic_auth(uri, user, password):
    password_mgr = urllib.request.HTTPPasswordMgrWithDefaultRealm()
    password_mgr.add_password(None, uri, user, password)
    auth_handler = urllib.request.HTTPBasicAuthHandler(password_mgr)
    opener = urllib.request.build_opener(auth_handler)
    urllib.request.install_opener(opener)


@click.command()
@click.option('base_uri', '--url', type=click.STRING, required=True, default='http://127.0.0.1:8080/',
              help='Base URL. (default: http://127.0.0.1:8080/)')
@click.option('--user', type=click.STRING, required=True,
              help='User name.')
@click.option('--password', type=click.STRING, required=True,
              help='User password.')
@click.option('module_id', '--module-id', type=UUID, required=True,
              help='Module UUID.')
@click.option('box_id', '--box-id', type=UUID, required=True,
              help='MessageBox UUID.')
@click.option('--start', type=click.STRING,
              help='Start date. (format: YYYYMMDD)')
@click.option('--end', type=click.STRING,
              help='End date. (format: YYYYMMDD)')
@click.option('filename', '-o', '--output', type=click.STRING,
              help='Output file name.')
def download(base_uri, user, password, module_id, box_id, start, end, filename):
    setup_basic_auth(base_uri, user, password)

    url = '{uri}/download/{module_id}/{box_id}/'.format(
        uri=base_uri,
        module_id=module_id, box_id=box_id,
    )
    query = []
    if start:
        query.append('start=' + start)
    if end:
        query.append('end=' + end)
    if len(query):
        url += '?' + '&'.join(query)

    if filename:
        urllib.request.urlretrieve(url, filename)
    else:
        response = urllib.request.urlopen(url).read()
        click.echo(response)


if __name__ == '__main__':
    download()
