from flask import Blueprint

__all__ = ('api',)

api = Blueprint('api', __name__)

from . import modules  # noqa
