import {LOCATION_CHANGE} from 'connected-react-router'
import {handleActions} from 'redux-actions'

import {actionTypes} from 'src/actions'


const initialState = {
  userEdit: {},
}

const initialize = () => (state, action) => ({
  ...initialState,
})

const error = handleActions({
  [LOCATION_CHANGE]: initialize(),
  [actionTypes.user.updateRequest]: (state, action) => {
    return {
      ...state,
      userEdit: {},
    }
  },
  [actionTypes.error.onUserUpdate]: (state, action) => {
    return {
      ...state,
      userEdit: action.payload,
    }
  },
}, initialState)

export default error
