# -*- coding: utf-8 -*-

"""WebUI Public Views."""

import logging

from flask import Blueprint


public = Blueprint('public', __name__)
logger = logging.getLogger(__name__)

from . import views  # noqa
