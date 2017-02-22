# -*- coding: utf-8 -*-

"""Flask download Blueprint."""

# system module
import logging

# community module
from flask import abort, Blueprint, request

# project module
from ..app import check_login


download = Blueprint('download', __name__)
logger = logging.getLogger(__name__)


@download.before_request
def before_request():
    token = request.args.get('access_token', None)
    if not token:
        raise abort(403)

    request.headers.environ['HTTP_AUTHORIZATION'] = 'Baerer {}'.format(token)
    check_login()
