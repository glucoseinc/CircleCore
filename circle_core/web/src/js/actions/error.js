import {createCcActions} from './utils'


const payloadCreators = {
  onUserUpdate: (errors) => errors,
}

const ccActions = createCcActions('error', payloadCreators)

export default ccActions.actions
export const actionTypes = ccActions.actionTypes
