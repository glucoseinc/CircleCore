import {createCcActions, nullPayloadCreator} from './utils'


const payloadCreators = {
  // Create
  createRequest: (rawSchema) => rawSchema,
  createSucceeded: (response) => response,
  createFailed: (message) => message,

  // Fetch
  fetchRequest: (params) => params.schemaId,
  fetchSucceeded: (response) => response,
  fetchFailed: (message) => message,

  // Fetch all
  fetchAllRequest: nullPayloadCreator,
  fetchAllSucceeded: (response) => response,
  fetchAllFailed: (message) => message,

  // Delete
  deleteRequest: (schemaId) => schemaId,
  deleteSucceeded: (response) => response,
  deleteFailed: (message) => message,
}

const ccActions = createCcActions('schema', payloadCreators)

export default ccActions.actions
export const actionTypes = ccActions.actionTypes
