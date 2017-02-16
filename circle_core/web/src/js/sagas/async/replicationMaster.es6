import CCAPI from 'src/api'
import actions, {actionTypes} from 'src/actions'

import {createAsyncSagaParam} from './utils'


const asyncSagaParams = {
  // Create
  [actionTypes.replicationMaster.createRequest]: createAsyncSagaParam(
      ::CCAPI.createReplicationMaster,
      (payload) => payload,
      actions.replicationMaster.createSucceeded,
      actions.replicationMaster.createFailed,
  ),

  // Fetch all
  [actionTypes.replicationMaster.fetchAllRequest]: createAsyncSagaParam(
    ::CCAPI.fetchAllReplicationMasters,
    () => null,
    actions.replicationMaster.fetchAllSucceeded,
    actions.replicationMaster.fetchAllFailed
  ),

  // Delete
  [actionTypes.replicationMaster.deleteRequest]: createAsyncSagaParam(
    ::CCAPI.deleteReplicationMaster,
    (payload) => payload,
    actions.replicationMaster.deleteSucceeded,
    actions.replicationMaster.deleteFailed,
  ),
}

export default asyncSagaParams
