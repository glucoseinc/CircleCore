import {createCcActions, nullPayloadCreator} from './utils'


const payloadCreators = {
  fetchRequest: (moduleId) => moduleId,
  fetchSucceeded: (response) => response,
  fetchFailed: (message) => message,

  update: (module) => module.toJS(),
  createInit: nullPayloadCreator,
}

const ccActions = createCcActions('module', payloadCreators)

export default ccActions.actions
export const actionTypes = ccActions.actionTypes
