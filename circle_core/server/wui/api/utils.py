# -*- coding: utf-8 -*-
from ..utils import (
    api_jsonify,
)


__all__ = (
    'respond_failure', 'respond_success'
)


def respond_failure(reason, _status=400, **kwargs):
    response = kwargs.copy()
    response['result'] = 'failure'
    response['detail'] = {
        'reason': reason,
    }
    return api_jsonify(_status=_status, **response)


def respond_success(**kwargs):
    response = kwargs.copy()
    response['result'] = 'success'

    return api_jsonify(_status=200, **response)
