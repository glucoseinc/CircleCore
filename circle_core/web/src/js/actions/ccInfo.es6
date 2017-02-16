import {createCcActions, nullPayloadCreator} from './utils'


const payloadCreators = {
  // Fetch myself
  fetchMyselfRequest: nullPayloadCreator,
  fetchMyselfSucceeded: (response) => response,
  fetchMyselfFailed: (message) => message,
}

const ccActions = createCcActions('ccInfo', payloadCreators)

export default ccActions.actions
export const actionTypes = ccActions.actionTypes
