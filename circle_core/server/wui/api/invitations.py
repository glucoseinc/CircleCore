# -*- coding: utf-8 -*-

"""招待関連APIの実装."""
import datetime

# community module
from flask import abort, request
from six import PY3

# project module
from circle_core.cli.utils import generate_uuid
from circle_core.models import Invitation
from .api import api
from .utils import respond_failure
from ..utils import (
    api_jsonify, convert_dict_key_camel_case, convert_dict_key_snake_case, get_metadata,
    oauth_require_read_users_scope, oauth_require_write_users_scope
)

if PY3:
    from typing import Any, Dict


@api.route('/invitations/', methods=['GET', 'POST'])
def api_invitations():
    if request.method == 'GET':
        return _get_invitations()
    if request.method == 'POST':
        return _post_invitation()
    abort(405)


@oauth_require_read_users_scope
def _get_invitations():
    invitations = get_metadata().invitations
    return api_jsonify(invitations=[obj.to_json() for obj in invitations])


@oauth_require_write_users_scope
def _post_invitation():
    # maxInvites項目しか許可しない
    obj = Invitation(None, request.json['maxInvites'], datetime.datetime.utcnow())

    metadata = get_metadata()
    metadata.register_invitation(obj)

    return api_jsonify(result='success', response=obj.to_json())


@api.route('/invitations/<obj_uuid>', methods=['DELETE'])
def api_invitation(obj_uuid):
    # if request.method == 'GET':
    #     return _get_module(module_uuid)
    # if request.method == 'PUT':
    #     return _put_module(module_uuid)
    if request.method == 'DELETE':
        return _delete_invitation(obj_uuid)
    abort(405)


@oauth_require_write_users_scope
def _delete_invitation(obj_uuid):
    # 自分は削除できない
    metadata = get_metadata()
    obj = metadata.find_invitation(obj_uuid)
    if obj is None:
        return respond_failure('Invitation not found.')

    # TODO(他のAPIの帰り値も合わせる)
    if not metadata.unregister_invitation(obj):
        return respond_failure('Invitation delete failed.')

    return api_jsonify(invitation={'uuid': obj.uuid})
