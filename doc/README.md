# Circle Core documentation
## Requirements
- Sphinx
- sphinx-rtd-theme

```
$ pip install -e '.[doc]'
```

## Usage

```
$ sphinx-apidoc -f -o source/apis ../circle_core
$ make clean && make html
```
