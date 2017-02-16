# -*- coding: utf-8 -*-
"""
"""
from flask import abort, render_template, request
import sqlalchemy.exc

from circle_core.models import Invitation, MetaDataSession, User
from . import public


@public.route('/invitation/<uuid:link_uuid>', methods=['GET', 'POST'])
def invitation_endpoint(link_uuid):
    invitation = Invitation.query.get(link_uuid)
    if not invitation or not invitation.can_invite():
        raise abort(404)

    error = None
    user = None
    is_completed = False
    if request.method == 'POST':
        form = request.form

        try:
            with MetaDataSession.begin():
                user = User.create(
                    account=form['account'],
                    work=form['work'],
                    telephone=form['telephone'],
                    mail_address=form['mailAddress'],
                )
                user.set_password(form['password'])
                invitation.inc_invites()

                MetaDataSession.add(user)
                MetaDataSession.add(invitation)
        except sqlalchemy.exc.IntegrityError:
            error = 'このアカウントはすでに使われています。'
        except ValueError as exc:
            error = str(exc)
        else:
            is_completed = True

    return render_template(
        'invitation.html',
        error=error, user=user.to_json() if user else None, is_completed=is_completed)
