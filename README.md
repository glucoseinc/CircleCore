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
