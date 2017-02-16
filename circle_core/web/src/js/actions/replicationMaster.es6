import {createCcActions, nullPayloadCreator} from './utils'


const payloadCreators = {
  // Create
  createRequest: (rawReplicationMaster) => rawReplicationMaster,
  createSucceeded: (response) => response,
  createFailed: (message) => message,

  // Fetch all
  fetchAllRequest: nullPayloadCreator,
  fetchAllSucceeded: (response) => response,
  fetchAllFailed: (message) => message,

  // Update
  deleteRequest: (rawReplicationMaster) => rawReplicationMaster,
  deleteSucceeded: (response) => response,
  deleteFailed: (message) => message,
}

const ccActions = createCcActions('replicationMaster', payloadCreators)

export default ccActions.actions
export const actionTypes = ccActions.actionTypes
