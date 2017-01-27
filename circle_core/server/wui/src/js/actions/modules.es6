import {createCcActions, nullPayloadCreator} from './utils'


const payloadCreators = {
  createRequest: (rawModule) => rawModule,
  createSucceeded: (response) => response,
  createFailed: (message) => message,

  fetchRequest: nullPayloadCreator,
  fetchSucceeded: (response) => response,
  fetchFailed: (message) => message,

  updateRequest: (rawModule) => rawModule,
  updateSucceeded: (response) => response,
  updateFailed: (message) => message,

  deleteAsk: (module) => module.toJS(),
  deleteCancel: nullPayloadCreator,
  deleteRequest: (moduleId) => moduleId,
  deleteSucceeded: (response) => response,
  deleteFailed: (message) => message,
}

const ccActions = createCcActions('modules', payloadCreators)

export default ccActions.actions
export const actionTypes = ccActions.actionTypes
