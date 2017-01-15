# -*- coding: utf-8 -*-
from ..utils import (
    api_jsonify, convert_dict_key_camel_case, convert_dict_key_snake_case,
)


__all__ = (
    'respond_failure', 'respond_success'
)


def respond_failure(reason):
    response = {}
    response['result'] = 'failure'
    response['detail'] = {
        'reason': reason,
    }
    return api_jsonify(_status=400, **convert_dict_key_camel_case(response))


def respond_success(detail):
    response = {}
    response['result'] = 'success'
    response['detail'] = detail
    return api_jsonify(**convert_dict_key_camel_case(response))
