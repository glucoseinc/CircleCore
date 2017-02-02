import {createCcActions} from './utils'


const payloadCreators = {
  setTitle: (title) => title,
  showSnackbar: (message) => message,
  hideSnackbar: () => null,
}

const ccActions = createCcActions('page', payloadCreators)

export default ccActions.actions
export const actionTypes = ccActions.actionTypes
