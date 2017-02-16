# -*- coding: utf-8 -*-

# community module
from flask import Response
from six import PY3

# project module
from ..utils import (
    api_jsonify,
)

if PY3:
    from typing import Dict


__all__ = (
    'respond_failure', 'respond_success'
)


def respond_failure(reason, _status=400, **kwargs):
    """失敗時のレスポンス.

    :param str reason: 失敗事由
    :param int _status: ステータスコード
    :param Dict kwargs: その他引数
    :return: レスポンス
    :rtype: Response
    """
    response = kwargs.copy()
    response['result'] = 'failure'
    response['detail'] = {
        'reason': reason,
    }
    return api_jsonify(_status=_status, **response)


def respond_success(**kwargs):
    """成功時のレスポンス.

    :param Dict kwargs: その他引数
    :return: レスポンス
    :rtype: Response
    """
    response = kwargs.copy()
    response['result'] = 'success'

    return api_jsonify(_status=200, **response)
