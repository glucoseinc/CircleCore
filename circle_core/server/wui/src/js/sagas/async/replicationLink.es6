import CCAPI from 'src/api'
import actions, {actionTypes} from 'src/actions'

import {createAsyncSagaParam} from './utils'


// Create
const replicationLinkCreateParam = createAsyncSagaParam(
  ::CCAPI.createReplicationLink,
  (payload) => payload,
  actions.replicationLinks.createSucceeded,
  actions.replicationLinks.createFailed
)

// Read all
const allReplicationLinksFetchParam = createAsyncSagaParam(
  ::CCAPI.fetchAllReplicationLinks,
  () => null,
  actions.replicationLinks.fetchSucceeded,
  actions.replicationLinks.fetchFailed
)

// Delete
const replicationLinkDeleteParam = createAsyncSagaParam(
  ::CCAPI.deleteReplicationLink,
  (payload) => payload,
  actions.replicationLinks.deleteSucceeded,
  actions.replicationLinks.deleteFailed
)

const asyncSagaParams = {
  // Create
  [actionTypes.replicationLinks.createRequest]: replicationLinkCreateParam,

  // Read all
  [actionTypes.replicationLinks.fetchRequest]: allReplicationLinksFetchParam,

  // Delete
  [actionTypes.replicationLinks.deleteRequest]: replicationLinkDeleteParam,
}

export default asyncSagaParams
