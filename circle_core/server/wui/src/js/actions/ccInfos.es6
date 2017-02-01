import {createCcActions, nullPayloadCreator} from './utils'


const payloadCreators = {
  // Fetch all
  fetchRequest: nullPayloadCreator,
  fetchSucceeded: (response) => response,
  fetchFailed: (message) => message,

  // Fetch myself
  fetchMyselfRequest: nullPayloadCreator,
  fetchMyselfSucceeded: (response) => response,
  fetchMyselfFailed: (message) => message,
}

const ccActions = createCcActions('ccInfos', payloadCreators)

export default ccActions.actions
export const actionTypes = ccActions.actionTypes
