import {createCcActions, nullPayloadCreator} from './utils'


const payloadCreators = {
  createRequest: (rawSchema) => rawSchema,
  createSucceeded: (response) => response,
  createFailed: (message) => message,

  fetchRequest: nullPayloadCreator,
  fetchSucceeded: (response) => response,
  fetchFailed: (message) => message,

  deleteRequest: (schemaId) => schemaId,
  deleteSucceeded: (response) => response,
  deleteFailed: (message) => message,
}

const ccActions = createCcActions('schemas', payloadCreators)

export default ccActions.actions
export const actionTypes = ccActions.actionTypes
