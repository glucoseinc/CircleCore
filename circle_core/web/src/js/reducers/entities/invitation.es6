import {actionTypes} from 'src/actions'

import {getNewEntities} from './utils'


const mergeInvitations = (state, action) => {
  const {
    invitations,
  } = getNewEntities(action.payload)
  return {
    ...state,
    invitations: state.invitations.merge(invitations),
  }
}

const refreshInvitations = (state, action) => {
  const {
    invitations,
  } = getNewEntities(action.payload)
  return {
    ...state,
    invitations,
  }
}

const deleteInvitations = (state, action) => {
  const {
    invitations,
  } = getNewEntities(action.payload)
  return {
    ...state,
    invitations: state.invitations.filterNot((invitation, invitationId) => invitations.keySeq().includes(invitationId)),
  }
}


const invitationActionsHandler = {
  // Create
  [actionTypes.invitation.createSucceeded]: mergeInvitations,

  // Fetch
  [actionTypes.invitation.fetchSucceeded]: mergeInvitations,

  // Fetch all
  [actionTypes.invitation.fetchAllSucceeded]: refreshInvitations,

  // Delete
  [actionTypes.invitation.deleteSucceeded]: deleteInvitations,
}

export default invitationActionsHandler
