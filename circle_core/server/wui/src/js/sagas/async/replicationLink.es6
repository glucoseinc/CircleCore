import CCAPI from 'src/api'
import actions, {actionTypes} from 'src/actions'

import {createAsyncSagaParam} from './utils'


// Create
const replicationLinkCreateParam = createAsyncSagaParam(
  ::CCAPI.createReplicationLink,
  (payload) => payload,
  actions.replicationLink.createSucceeded,
  actions.replicationLink.createFailed
)

// Fetch all
const allReplicationLinksFetchParam = createAsyncSagaParam(
  ::CCAPI.fetchAllReplicationLinks,
  () => null,
  actions.replicationLink.fetchAllSucceeded,
  actions.replicationLink.fetchAllFailed
)

// Delete
const replicationLinkDeleteParam = createAsyncSagaParam(
  ::CCAPI.deleteReplicationLink,
  (payload) => payload,
  actions.replicationLink.deleteSucceeded,
  actions.replicationLink.deleteFailed
)

const asyncSagaParams = {
  // Create
  [actionTypes.replicationLink.createRequest]: replicationLinkCreateParam,

  // Fetch all
  [actionTypes.replicationLink.fetchAllRequest]: allReplicationLinksFetchParam,

  // Delete
  [actionTypes.replicationLink.deleteRequest]: replicationLinkDeleteParam,
}

export default asyncSagaParams
