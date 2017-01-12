import {createCcActions, nullPayloadCreator} from './utils'

const ccActions = createCcActions('schemas', {
  // createRequest: (schema) => schema.toJS(),
  // createSucceeded: (response) => response,
  // createFailed: (message) => message,

  fetchRequest: nullPayloadCreator,
  fetchSucceeded: (users) => users.map((users) => users.toJS()),
  fetchFailed: (message) => message,

  // deleteAsk: (schema) => schema.toJS(),
  // deleteCancel: nullPayloadCreator,
  // deleteRequest: (schema) => schema.toJS(),
  // deleteSucceeded: (response) => response,
  // deleteFailed: (message) => message,
})

export default ccActions.actions
export const actionTypes = ccActions.actionTypes
