import {createCcActions, nullPayloadCreator, passPayloadCreator} from './utils'

const ccActions = createCcActions('users', {
  fetchRequest: nullPayloadCreator,
  fetchSucceeded: (users) => users.map((user) => user.toJS()),
  fetchFailed: (message) => message,

  deleteRequest: (user) => user.toJS(),
  deleteComplete: passPayloadCreator,
})

export default ccActions.actions
export const actionTypes = ccActions.actionTypes
