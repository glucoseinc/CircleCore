# -*- coding: utf-8 -*-
from ..utils import (
    api_jsonify, convert_dict_key_camel_case,
)


__all__ = (
    'respond_failure'
)


def respond_failure(reason):
    response = {}
    response['result'] = 'failure'
    response['detail'] = {
        'reason': reason,
    }
    return api_jsonify(_status=400, **convert_dict_key_camel_case(response))
