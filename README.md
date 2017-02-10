[![CircleCI](https://circleci.com/gh/glucoseinc/CircleCore.svg?style=svg&circle-token=13e263f3101ee208b64500d73c5f3741a8c8aa97)](https://circleci.com/gh/glucoseinc/CircleCore)

# CircleCore
## Requirements
- Python2.7 or Python3.5
- nanomsg
    - https://github.com/nanomsg/nanomsg
- MySQL

## Getting Strarted
- [Mac](INSTALL_MACOSX.md)

## Installation
### Setup virtualenv
- Python2
```bash
$ virtualenv -p path/to/python2.7 .env/2.7
$ . .env/2.7/bin/activate
(2.7) $
```

- Python3
```bash
$ virtualenv -p path/to/python3.5 .env/3.5
$ . .env/3.5/bin/activate
(3.5) $
```

### Install CircleCore
```bash
$ pip install -e git://github.com/nanomsg/nnpy.git#egg=nnpy
$ pip install http://cdn.mysql.com//Downloads/Connector-Python/mysql-connector-python-2.2.1.tar.gz
$ pip install '.[test,mysql]'
```

If you want to install CircleCore as development, use `-e` option.


## Usage
### Set environment variable
```bash
$ export CRCR_UUID=...
$ export CRCR_DATABASE=mysql+mysqlconnector://root@localhost/crcr
```

or grant arguments at command excution.
```bash
$ crcr subcommand
```

### Setup SSL certificate
0. キーチェーンアクセス.appを起動
0. メニューバーのファイル -> 読み込む...をクリック
0. CircleCore/tests/tls.crtを選択
0. 検索窓にglucoseと入力、名前がglucoseの証明書を見つけてダブルクリック
0. ▶信頼を開いて常に信頼を選択

Chrome等だと自己証明している証明書には安全でない旨警告が出るが、それを無視すれば問題ない。
curlは問題なく通る。

### Run server
```bash
$ crcr server run
```

### Build document
```bash
$ tox -e sphinx
```

## Development

### Setup

```bash
$ npm install
```

### Build JS & CSS

```bash
$ npm run build
```

watch changes & rebuild
```bash
$ npm run watch
```

see doc/README.md .
