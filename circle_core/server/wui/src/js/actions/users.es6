import {createCcActions, nullPayloadCreator, passPayloadCreator, toJSPayloadCreator} from './utils'

const ccActions = createCcActions('users', {
  fetchRequest: nullPayloadCreator,
  fetchComplete: passPayloadCreator,

  deleteRequest: toJSPayloadCreator,
  deleteComplete: passPayloadCreator,

  fetchMeRequest: nullPayloadCreator,
  fetchMeComplete: passPayloadCreator,
})

export default ccActions.actions
export const actionTypes = ccActions.actionTypes
