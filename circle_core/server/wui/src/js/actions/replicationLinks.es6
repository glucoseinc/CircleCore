import {createCcActions, nullPayloadCreator} from './utils'


const payloadCreators = {
  // Create
  createRequest: (rawReplicationLink) => rawReplicationLink,
  createSucceeded: (response) => response,
  createFailed: (message) => message,

  // Fetch all
  fetchRequest: nullPayloadCreator,
  fetchSucceeded: (response) => response,
  fetchFailed: (message) => message,

  // Delete
  deleteRequest: (replicationLinkId) => replicationLinkId,
  deleteSucceeded: (response) => response,
  deleteFailed: (message) => message,
}

const ccActions = createCcActions('replicationLinks', payloadCreators)

export default ccActions.actions
export const actionTypes = ccActions.actionTypes
