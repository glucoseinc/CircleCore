[![CircleCI](https://circleci.com/gh/glucoseinc/CircleCore.svg?style=svg&circle-token=13e263f3101ee208b64500d73c5f3741a8c8aa97)](https://circleci.com/gh/glucoseinc/CircleCore)

# Circle Core
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

### Install Circle Core
```bash
$ pip install -e .
```

### For development
```bash
$ pip install pip-tools
$ pip-sync requirements2.txt  # for Python2. If you use Python3, "$ pip-sync requirements3.txt"
$ pip install -e .
```

#### Update requirements.txt
- When editted `requirements.in`, execute the following.
```bash
(2.7) $ pip-compile -o requirements2.txt  # for Python2.
(3.5) $ pip-compile -o requirements3.txt  # for Python3.
```

## Usage
```bash
$ crcr --config redis://localhost:6379/0 --uuid ... server run
```
