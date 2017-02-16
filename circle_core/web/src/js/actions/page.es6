import {createCcActions} from './utils'


const payloadCreators = {
  // Title
  setTitle: (title) => title,

  // Snackbar
  showSnackbar: (message) => message,
  hideSnackbar: () => null,

  // ErrorDialog
  showErrorDialog: (payload) => (payload),
  hideErrorDialog: () => null,
}

const ccActions = createCcActions('page', payloadCreators)

export default ccActions.actions
export const actionTypes = ccActions.actionTypes
