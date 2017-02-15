import CCAPI from 'src/api'
import actions, {actionTypes} from 'src/actions'

import {createAsyncSagaParam} from './utils'


// Create
const invitationCreateParam = createAsyncSagaParam(
    ::CCAPI.createInvitation,
    (payload) => payload,
    actions.invitation.createSucceeded,
    actions.invitation.createFailed,
)

// Fetch
const invitationFetchParam = createAsyncSagaParam(
  ::CCAPI.fetchInvitation,
  (payload) => payload,
  actions.invitation.fetchSucceeded,
  actions.invitation.fetchFailed
)

// Fetch all
const allInvitationsFetchParam = createAsyncSagaParam(
  ::CCAPI.fetchAllInvitations,
  () => null,
  actions.invitation.fetchAllSucceeded,
  actions.invitation.fetchAllFailed
)

// Delete
const invitationDeleteParam = createAsyncSagaParam(
  ::CCAPI.deleteInvitation,
  (payload) => payload,
  actions.invitation.deleteSucceeded,
  actions.invitation.deleteFailed,
)


const asyncSagaParams = {
  // Create
  [actionTypes.invitation.createRequest]: invitationCreateParam,

  // Fetch
  [actionTypes.invitation.fetchRequest]: invitationFetchParam,

  // Fetch all
  [actionTypes.invitation.fetchAllRequest]: allInvitationsFetchParam,

  // Delete
  [actionTypes.invitation.deleteRequest]: invitationDeleteParam,
}

export default asyncSagaParams
