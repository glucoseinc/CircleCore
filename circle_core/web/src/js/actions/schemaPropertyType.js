import {createCcActions, nullPayloadCreator} from './utils'


const payloadCreators = {
  fetchAllRequest: nullPayloadCreator,
  fetchAllSucceeded: (response) => response,
  fetchAllFailed: (message) => message,
}

const ccActions = createCcActions('schemaPropertyType', payloadCreators)

export default ccActions.actions
export const actionTypes = ccActions.actionTypes
