# -*- coding: utf-8 -*-

"""招待関連APIの実装."""

# system module
import datetime

# community module
from flask import abort, request

# project module
from circle_core.models import generate_uuid, Invitation, MetaDataSession
from .api import api
from .utils import respond_failure, respond_success
from ..utils import (
    oauth_require_read_users_scope, oauth_require_write_users_scope
)


@api.route('/invitations/', methods=['GET', 'POST'])
def api_invitations():
    """全てのInvitationのCRUD."""
    if request.method == 'GET':
        return _get_invitations()
    if request.method == 'POST':
        return _post_invitation()
    abort(405)


@oauth_require_read_users_scope
def _get_invitations():
    """全てのInvitationの情報を取得する.

    :return: 全てのInvitationの情報
    :rtype: Response
    """
    return respond_success(invitations=[obj.to_json() for obj in Invitation.query])


@oauth_require_write_users_scope
def _post_invitation():
    """Invitationを作成する.

    :return: 作成したInvitationの情報
    :rtype: Response
    """
    # maxInvites項目しか許可しない
    with MetaDataSession.begin():
        obj = Invitation(
            uuid=generate_uuid(model=Invitation),
            max_invites=request.json['maxInvites'],
            created_at=datetime.datetime.utcnow()
        )
        MetaDataSession.add(obj)

    return respond_success(invitation=obj.to_json())


@api.route('/invitations/<obj_uuid>', methods=['DELETE'])
def api_invitation(obj_uuid):
    """単一のInvitationのCRUD."""
    invitation = Invitation.query.get(obj_uuid)
    if not invitation:
        return respond_failure('not found', _status=404)

    # if request.method == 'GET':
    #     return _get_module(module_uuid)
    # if request.method == 'PUT':
    #     return _put_module(module_uuid)
    if request.method == 'DELETE':
        return _delete_invitation(invitation)
    abort(405)


@oauth_require_write_users_scope
def _delete_invitation(invitation):
    """Invitationを削除する.

    :param Invitation invitation: 削除するInvitation
    :return: Invitationの情報
    :rtype: Response
    """
    with MetaDataSession.begin():
        MetaDataSession.delete(invitation)

    return respond_success(invitation={'uuid': invitation.uuid})
