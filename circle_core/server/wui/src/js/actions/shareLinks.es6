import {createCcActions} from './utils'


const payloadCreators = {
  createRequest: (something) => something,
  createSucceeded: (response) => response,
  createFailed: (message) => message,
}

const ccActions = createCcActions('shareLink', payloadCreators)

export default ccActions.actions
export const actionTypes = ccActions.actionTypes
