# -*- coding: utf-8 -*-

"""Flask api Blueprint."""

# community module
import datetime

from flask import Blueprint

api = Blueprint('api', __name__)


@api.before_request
def before_request():
    """ログイン確認"""
    from ..authorize.core import oauth
    from ..utils import get_metadata

    t, oauth_requets = oauth.verify_request([])
    my_uuid = oauth_requets.user

    metadata = get_metadata()
    metadata.update_user_last_access(my_uuid, datetime.datetime.utcnow())
