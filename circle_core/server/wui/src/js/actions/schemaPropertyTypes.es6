import {createCcActions, nullPayloadCreator} from './utils'


const payloadCreators = {
  fetchRequest: nullPayloadCreator,
  fetchSucceeded: (response) => response,
  fetchFailed: (message) => message,
}

const ccActions = createCcActions('schemaPropertyTypes', payloadCreators)

export default ccActions.actions
export const actionTypes = ccActions.actionTypes
