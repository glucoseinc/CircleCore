import {createCcActions} from './utils'


const payloadCreators = {
  fetchRequest: (params) => params.schemaId,
  fetchSucceeded: (response) => response,
  fetchFailed: (message) => message,
}

const ccActions = createCcActions('schema', payloadCreators)

export default ccActions.actions
export const actionTypes = ccActions.actionTypes
