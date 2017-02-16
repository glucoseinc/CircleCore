import {createCcActions, passPayloadCreator} from './utils'


const ccActions = createCcActions('auth', {
  loginSucceeded: passPayloadCreator,
  loginFailed: passPayloadCreator,

  tokenInvalidated: passPayloadCreator,
})

export default ccActions.actions
export const actionTypes = ccActions.actionTypes
