# -*- coding: utf-8 -*-
"""
"""
from flask import abort, render_template

from circle_core.models import Invitation
from . import public, logger


@public.route('/invitation/<uuid:link_uuid>')
def invitation_endpoint(link_uuid):
    invitation = Invitation.query.get(link_uuid)
    if not invitation or not invitation.can_invite():
        raise abort(404)

    return render_template('invitation.html')
