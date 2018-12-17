# -*- coding: utf-8 -*-
"""WebUI API Utilities."""

from typing import TYPE_CHECKING

# project module
from ..utils import (
    api_jsonify,
)

# type annotation
if TYPE_CHECKING:
    from typing import Any

    from flask import Response

__all__ = ('respond_failure', 'respond_success')


def respond_failure(reason: str, _status: int = 400, **kwargs: 'Any') -> 'Response':
    """失敗時のレスポンス.

    Args:
        reason: 失敗事由
        _status: ステータスコード
        kwargs: その他引数

    Return:
        レスポンス
    """
    response = kwargs.copy()
    response['result'] = 'failure'
    response['detail'] = {
        'reason': reason,
    }
    return api_jsonify(_status=_status, **response)


def respond_success(**kwargs: 'Any') -> 'Response':
    """成功時のレスポンス.

    Args:
        kwargs: その他引数
    Return:
        レスポンス
    """
    response = kwargs.copy()
    response['result'] = 'success'

    return api_jsonify(_status=200, **response)
