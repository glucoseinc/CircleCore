import {handleActions} from 'redux-actions'

import {actionTypes} from 'src/actions'

const initialState = {
  isSnackbarOpen: false,
  title: '',
  snackbarMessage: '',
}


const page = handleActions({
  [actionTypes.page.setTitle]: (state, action) => {
    const title = action.payload
    return {
      ...state,
      title,
    }
  },

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
}, initialState)

export default page
