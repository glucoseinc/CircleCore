import {createCcActions, nullPayloadCreator, passPayloadCreator, toJSPayloadCreator} from './utils'

const ccActions = createCcActions('invitations', {
  createRequest: passPayloadCreator,
  createComplete: passPayloadCreator,

  deleteRequest: toJSPayloadCreator,
  deleteComplete: passPayloadCreator,

  fetchRequest: nullPayloadCreator,
  fetchComplete: passPayloadCreator,
})

export default ccActions.actions
export const actionTypes = ccActions.actionTypes
