import {createCcActions, nullPayloadCreator} from './utils'


const payloadCreators = {
  clearErrorMessage: nullPayloadCreator,
}

const ccActions = createCcActions('misc', payloadCreators)

export default ccActions.actions
export const actionTypes = ccActions.actionTypes
