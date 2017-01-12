import {createCcActions, nullPayloadCreator} from './utils'

const ccActions = createCcActions('users', {
  fetchRequest: nullPayloadCreator,
  fetchSucceeded: (users) => users.map((user) => user.toJS()),
  fetchFailed: (message) => message,
})

export default ccActions.actions
export const actionTypes = ccActions.actionTypes
