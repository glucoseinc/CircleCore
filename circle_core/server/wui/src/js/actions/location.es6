import {createCcActions, nullPayloadCreator} from './utils'


const payloadCreators = {
  changeRequest: (pathname) => pathname,
  changeCancel: nullPayloadCreator,
}

const ccActions = createCcActions('location', payloadCreators)

export default ccActions.actions
export const actionTypes = ccActions.actionTypes
