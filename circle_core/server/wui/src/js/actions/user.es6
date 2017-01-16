import {createCcActions, nullPayloadCreator, passPayloadCreator} from './utils'


const ccActions = createCcActions('user', {
  update: (user) => user.toJS(),
  createInit: nullPayloadCreator,

  updateRequest: passPayloadCreator,
  updateComplete: passPayloadCreator,
})

export default ccActions.actions
export const actionTypes = ccActions.actionTypes
