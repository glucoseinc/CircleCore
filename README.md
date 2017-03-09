[![CircleCI](https://circleci.com/gh/glucoseinc/CircleCore.svg?style=svg&circle-token=13e263f3101ee208b64500d73c5f3741a8c8aa97)](https://circleci.com/gh/glucoseinc/CircleCore)

# CircleCore
## Requirements
- Python3.5
- nanomsg
    - https://github.com/nanomsg/nanomsg
- MySQL

## Getting Started
- [Mac](INSTALL_MACOSX.md)

## Installation
### Setup virtualenv
```bash
$ virtualenv -p path/to/python3.5 .env
$ . .env/bin/activate
(.env) $
```

### Install CircleCore
```bash
$ python setup.py develop
```

or

```bash
$ pip install -e git://github.com/nanomsg/nnpy.git#egg=nnpy
$ pip install -e git://github.com/graphite-project/whisper.git@b783ab3f577f3f60db607adda241e29b7242bcf4#egg=whisper-0.10.0rc1
$ pip install -e '.[test]'
```


## Usage
### Run server
```bash
$ crcr run
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
