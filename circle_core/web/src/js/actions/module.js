import {createCcActions, nullPayloadCreator} from './utils'


const payloadCreators = {
  // Create
  createRequest: (rawModule) => rawModule,
  createSucceeded: (response) => response,
  createFailed: (message) => message,

  // Fetch
  fetchRequest: (params) => params.moduleId,
  fetchSucceeded: (response) => response,
  fetchFailed: (message) => message,

  // Fetch all
  fetchAllRequest: nullPayloadCreator,
  fetchAllSucceeded: (response) => response,
  fetchAllFailed: (message) => message,

  // Update
  updateRequest: (rawModule) => rawModule,
  updateSucceeded: (response) => response,
  updateFailed: (message) => message,

  // Delete
  deleteRequest: (moduleId) => moduleId,
  deleteSucceeded: (response) => response,
  deleteFailed: (message) => message,
}

const ccActions = createCcActions('module', payloadCreators)

export default ccActions.actions
export const actionTypes = ccActions.actionTypes
