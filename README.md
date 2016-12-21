[![CircleCI](https://circleci.com/gh/glucoseinc/CircleCore.svg?style=svg&circle-token=13e263f3101ee208b64500d73c5f3741a8c8aa97)](https://circleci.com/gh/glucoseinc/CircleCore)

# CircleCore
## Requirements
- Python2.7 or Python3.5
- nanomsg
    - https://github.com/nanomsg/nanomsg
- MySQL

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
$ pip install '.[test,redis,mysql]'
```

If you want to install CircleCore as development, use `-e` option.


## Usage
### Set environment variable
```bash
$ export CRCR_METADATA=redis://localhost:6379/0
$ export CRCR_UUID=...
$ export CRCR_DATABASE=mysql+mysqlconnector://root@localhost/crcr
```

or grant arguments at command excution.
```bash
$ crcr --metadata redis://localhost:6379/0 --uuid ... subcommand
```

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
