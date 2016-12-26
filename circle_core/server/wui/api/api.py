# -*- coding: utf-8 -*-

"""Flask api Blueprint."""

# community module
from flask import Blueprint


api = Blueprint('api', __name__, url_prefix='/api')
