import {createCcActions} from './utils'


const payloadCreators = {
  setTitle: (title) => title,
}

const ccActions = createCcActions('page', payloadCreators)

export default ccActions.actions
export const actionTypes = ccActions.actionTypes
