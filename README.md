[![CircleCI](https://circleci.com/gh/glucoseinc/CircleCore.svg?style=svg&circle-token=13e263f3101ee208b64500d73c5f3741a8c8aa97)](https://circleci.com/gh/glucoseinc/CircleCore)

# CircleCore
## Requirements
- Python2.7 or Python3.5
- nanomsg
    - https://github.com/nanomsg/nanomsg

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

If you want to install CircleCore as development, use `-e` option


## Usage
```bash
$ crcr --config redis://localhost:6379/0 --uuid ... server run
```
