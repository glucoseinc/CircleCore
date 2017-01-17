# -*- coding:utf-8 -*-

# system module
import datetime

# community module
import dateutil.parser
import dateutil.tz


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
