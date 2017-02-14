import {actionTypes} from 'src/actions'

import {changeFlagAction} from './utils'


const invitationActionsHandler = {
  // Fetch all
  [actionTypes.invitations.fetchRequest]: changeFlagAction('isInvitationsFetching', true),
  [actionTypes.invitations.fetchComplete]: changeFlagAction('isInvitationsFetching', false),
}

export default invitationActionsHandler
