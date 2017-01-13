import {createCcActions, nullPayloadCreator} from './utils'


const payloadCreators = {
  fetchRequest: (schemaId) => schemaId,
  fetchSucceeded: (response) => response,
  fetchFailed: (message) => message,

  update: (schema) => schema.toJS(),
  createInit: nullPayloadCreator,
}

const ccActions = createCcActions('schema', payloadCreators)

export default ccActions.actions
export const actionTypes = ccActions.actionTypes
