import {createCcActions, nullPayloadCreator} from './utils'


const ccActions = createCcActions('user', {
  update: (user) => user.toJS(),
  createInit: nullPayloadCreator,
})

export default ccActions.actions
export const actionTypes = ccActions.actionTypes
