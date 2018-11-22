import {handleActions} from 'redux-actions'

import {actionTypes} from 'src/actions'

const initialState = {
  title: '',

  isSnackbarOpen: false,
  snackbarMessage: '',

  isErrorDialogOpen: false,
  errorDialogMessages: {},
}


const page = handleActions({
  // Title
  [actionTypes.page.setTitle]: (state, action) => {
    const title = action.payload
    return {
      ...state,
      title,
    }
  },

  // Snackbar
  [actionTypes.page.showSnackbar]: (state, action) => {
    const snackbarMessage= action.payload
    return {
      ...state,
      isSnackbarOpen: true,
      snackbarMessage,
    }
  },

  [actionTypes.page.hideSnackbar]: (state, action) => {
    return {
      ...state,
      isSnackbarOpen: false,
      snackbarMessage: '',
    }
  },

  // ErrorDialog
  [actionTypes.page.showErrorDialog]: (state, action) => {
    return {
      ...state,
      isErrorDialogOpen: true,
      errorDialogMessages: action.payload,
    }
  },

  [actionTypes.page.hideErrorDialog]: (state, action) => {
    return {
      ...state,
      isErrorDialogOpen: false,
      errorDialogMessages: {},
    }
  },
}, initialState)

export default page
