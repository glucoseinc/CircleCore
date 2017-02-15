import {actionTypes} from 'src/actions'

import {changeFlagAction} from './utils'


const invitationActionsHandler = {
  // Create
  [actionTypes.invitation.createRequest]: changeFlagAction('isInvitationCreating', true),
  [actionTypes.invitation.createSucceeded]: changeFlagAction('isInvitationCreating', false),
  [actionTypes.invitation.createFailed]: changeFlagAction('isInvitationCreating', false),

  // Fetch
  [actionTypes.invitation.fetchRequest]: changeFlagAction('isInvitationFetching', true),
  [actionTypes.invitation.fetchSucceeded]: changeFlagAction('isInvitationFetching', false),
  [actionTypes.invitation.fetchFailed]: changeFlagAction('isInvitationFetching', false),

  // Fetch all
  [actionTypes.invitation.fetchAllRequest]: changeFlagAction('isInvitationFetching', true),
  [actionTypes.invitation.fetchAllSucceeded]: changeFlagAction('isInvitationFetching', false),
  [actionTypes.invitation.fetchAllFailed]: changeFlagAction('isInvitationFetching', false),

  // Delete
  [actionTypes.invitation.deleteRequest]: changeFlagAction('isInvitationDeleting', true),
  [actionTypes.invitation.deleteSucceeded]: changeFlagAction('isInvitationDeleting', false),
  [actionTypes.invitation.deleteFailed]: changeFlagAction('isInvitationDeleting', false),
}

export default invitationActionsHandler
