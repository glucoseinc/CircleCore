import {createCcActions} from './utils'


const payloadCreators = {
  fetchRequest: (params) => params.moduleId,
  fetchSucceeded: (response) => response,
  fetchFailed: (message) => message,
}

const ccActions = createCcActions('module', payloadCreators)

export default ccActions.actions
export const actionTypes = ccActions.actionTypes
