import {createCcActions, nullPayloadCreator} from './utils'


const payloadCreators = {
  createRequest: (module) => module.toJS(),
  createSucceeded: (response) => response,
  createFailed: (message) => message,

  fetchRequest: nullPayloadCreator,
  fetchSucceeded: (response) => response,
  fetchFailed: (message) => message,

  updateRequest: (module) => module.toJS(),
  updateSucceeded: (response) => response,
  updateFailed: (message) => message,

  deleteAsk: (module) => module.toJS(),
  deleteCancel: nullPayloadCreator,
  deleteRequest: (module) => module.toJS(),
  deleteSucceeded: (response) => response,
  deleteFailed: (message) => message,
}

const ccActions = createCcActions('modules', payloadCreators)

export default ccActions.actions
export const actionTypes = ccActions.actionTypes
