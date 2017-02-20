# -*- coding: utf-8 -*-

"""Flask api Blueprint."""

# community module
import datetime
import logging

from flask import abort, Blueprint

api = Blueprint('api', __name__)
logger = logging.getLogger(__name__)


@api.before_request
def before_request():
    """ログイン確認"""
    from ..authorize.core import oauth

    t, oauth_requets = oauth.verify_request([])
    user = oauth_requets.user

    if not user:
        raise abort(403)

    # update user's last access
    from circle_core.models import MetaDataSession

    with MetaDataSession.begin():
        user.last_access_at = datetime.datetime.utcnow()
        MetaDataSession.add(user)
