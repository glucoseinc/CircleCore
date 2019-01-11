import {createCcActions, nullPayloadCreator} from './utils'


const payloadCreators = {
  // Create
  createRequest: (rawUser) => rawUser,
  createSucceeded: (response) => response,
  createFailed: (message) => message,

  // Fetch
  fetchRequest: (params) => params.userId,
  fetchSucceeded: (response) => response,
  fetchFailed: (message) => message,

  // Fetch all
  fetchAllRequest: nullPayloadCreator,
  fetchAllSucceeded: (response) => response,
  fetchAllFailed: (message) => message,

  // Fetch myself
  fetchMyselfRequest: nullPayloadCreator,
  fetchMyselfSucceeded: (response) => response,
  fetchMyselfFailed: (message) => message,

  // Fetch token
  fetchTokenRequest: (params) => params.userId,
  fetchTokenSucceeded: (response) => response,
  fetchTokenFailed: (message) => message,

  // Update
  updateRequest: (rawUser) => rawUser,
  updateSucceeded: (response) => response,
  updateFailed: (message) => message,

  // Generate token
  generateTokenRequest: (userId) => userId,
  generateTokenSucceeded: (response) => response,
  generateTokenFailed: (message) => message,

  // Delete
  deleteRequest: (userId) => userId,
  deleteSucceeded: (response) => response,
  deleteFailed: (message) => message,
}

const ccActions = createCcActions('user', payloadCreators)

export default ccActions.actions
export const actionTypes = ccActions.actionTypes
