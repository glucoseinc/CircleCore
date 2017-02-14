import {createCcActions, nullPayloadCreator} from './utils'


const payloadCreators = {
  // Create
  createRequest: (rawSchema) => rawSchema,
  createSucceeded: (response) => response,
  createFailed: (message) => message,

  createdDialogClose: () => null,

  // Fetch
  fetchRequest: (params) => params.invitationId,
  fetchSucceeded: (response) => response,
  fetchFailed: (message) => message,

  // Fetch all
  fetchAllRequest: nullPayloadCreator,
  fetchAllSucceeded: (response) => response,
  fetchAllFailed: (message) => message,

  // Delete
  deleteRequest: (invitationId) => invitationId,
  deleteSucceeded: (response) => response,
  deleteFailed: (message) => message,
}

const ccActions = createCcActions('invitation', payloadCreators)

export default ccActions.actions
export const actionTypes = ccActions.actionTypes
