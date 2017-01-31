import {handleActions} from 'redux-actions'
import {LOCATION_CHANGE} from 'react-router-redux'

import {actionTypes} from 'src/actions'


const initialState = {
  errorMessage: null,
}


const initialize = () => (state, action) => ({
  ...initialState,
})


const misc = handleActions({
  // Location change
  [LOCATION_CHANGE]: initialize(),

  // User
  [actionTypes.users.deleteComplete]: (state, {payload: {error}}) => {
    if(error)
      return {...state, errorMessage: error.message}
    return state
  },

  [actionTypes.misc.clearErrorMessage]: (state, action) => {
    return {
      ...state,
      errorMessage: action.payload,
    }
  },
}, initialState)

export default misc
