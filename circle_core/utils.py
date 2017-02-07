# -*- coding:utf-8 -*-

# system module
import datetime
import os
import subprocess
import sys
import uuid

# community module
import dateutil.parser
import dateutil.tz
import six


def prepare_uuid(v):
    if not v:
        return None
    if not isinstance(v, uuid.UUID):
        v = uuid.UUID(v)
    return v


def prepare_date(v):
    if not v:
        return v
    if isinstance(v, str):
        v = dateutil.parser.parse(v)
        if not v:
            raise ValueError('invalid datet time format {!r}'.format(v))
    if not v.tzinfo:
        # naiveな日付は、ローカル日付として扱う
        v = v.replace(tzinfo=dateutil.tz.tzlocal())
    # 最終的にUTCにする
    v = v.astimezone(dateutil.tz.tzutc())
    return v


def format_date(v):
    assert v is None or isinstance(v, datetime.datetime)

    if not v:
        return None
    return v.isoformat('T')


# popen
def portable_popen(cmd, *args, **kwargs):
    """A portable version of subprocess.Popen that automatically locates
    executables before invoking them.  This also looks for executables
    in the bundle bin.
    """
    if cmd[0] is None:
        raise RuntimeError('No executable specified')
    exe = locate_executable(cmd[0], kwargs.get('cwd'))
    if exe is None:
        raise RuntimeError('Could not locate executable "%s"' % cmd[0])

    if isinstance(exe, six.text_type):
        exe = exe.encode(sys.getfilesystemencoding())
    cmd[0] = exe

    return subprocess.Popen(cmd, *args, **kwargs)


def locate_executable(exe_file, cwd=None):
    """Locates an executable in the search path."""
    choices = [exe_file]
    resolve = True

    # If it's already a path, we don't resolve.
    if os.path.sep in exe_file or \
       (os.path.altsep and os.path.altsep in exe_file):
        resolve = False

    extensions = os.environ.get('PATHEXT', '').split(';')
    _, ext = os.path.splitext(exe_file)
    if os.name != 'nt' and '' not in extensions or \
       any(ext.lower() == extension.lower() for extension in extensions):
        extensions.insert(0, '')

    if resolve:
        paths = os.environ.get('PATH', '').split(os.pathsep)
        choices = [os.path.join(path, exe_file) for path in paths]

    if os.name == 'nt':
        choices.append(os.path.join((cwd or os.getcwd()), exe_file))

    try:
        for path in choices:
            for ext in extensions:
                if os.access(path + ext, os.X_OK):
                    return path + ext
    except OSError:
        pass
