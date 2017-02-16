import {createCcActions, nullPayloadCreator} from './utils'


const payloadCreators = {
  // Fetch all
  fetchAllRequest: nullPayloadCreator,
  fetchAllSucceeded: (response) => response,
  fetchAllFailed: (message) => message,

  // Fetch myself
  fetchMyselfRequest: nullPayloadCreator,
  fetchMyselfSucceeded: (response) => response,
  fetchMyselfFailed: (message) => message,

  // Update
  updateRequest: (rawCcInfo) => rawCcInfo,
  updateSucceeded: (response) => response,
  updateFailed: (message) => message,
}

const ccActions = createCcActions('ccInfo', payloadCreators)

export default ccActions.actions
export const actionTypes = ccActions.actionTypes
