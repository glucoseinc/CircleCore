# -*- coding: utf-8 -*-
"""Flask api Blueprint."""

# system module
import logging

# community module
from flask import Blueprint

# project module
from ..app import check_login

api = Blueprint('api', __name__)
logger = logging.getLogger(__name__)


@api.before_request
def before_request():
    """リクエスト前に呼ばれる."""
    check_login()
