import {createCcActions, nullPayloadCreator} from './utils'


const payloadCreators = {
  createRequest: (module) => module.toJS(),
  createSucceeded: (response) => response,
  createFailed: (message) => message,

  fetchRequest: nullPayloadCreator,
  fetchSucceeded: (modules) => modules.map((module) => module.toJS()),
  fetchFailed: (message) => message,

  deleteAsk: (module) => module.toJS(),
  deleteCancel: nullPayloadCreator,
  deleteRequest: (module) => module.toJS(),
  deleteSucceeded: (response) => response,
  deleteFailed: (message) => message,
}

const ccActions = createCcActions('modules', payloadCreators)

export default ccActions.actions
export const actionTypes = ccActions.actionTypes
