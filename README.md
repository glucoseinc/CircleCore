# Circle Core
## Requirements
- nanomsg
    - https://github.com/nanomsg/nanomsg

## Installation
```bash
$ pip install -e .
```

### For development
```bash
$ pip install pip-tools
$ pip-sync requirements2.txt  # python2
$ pip install -e .
```

## Usage
```bash
$ crcr --config redis://localhost:6379/0 --uuid ... server run
```
