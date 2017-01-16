import {createCcActions, passPayloadCreator} from './utils'


const ccActions = createCcActions('auth', {
  loginSucceeded: passPayloadCreator,
  loginFailed: passPayloadCreator,
})

export default ccActions.actions
export const actionTypes = ccActions.actionTypes
