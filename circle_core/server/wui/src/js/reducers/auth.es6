import {handleActions} from 'redux-actions'
import {LOCATION_CHANGE} from 'react-router-redux'

import {actionTypes} from '../actions'
import CCAPI from '../api'
import {oauthToken} from '../Authorization'

const initialState = {
  token: oauthToken,
  tokenLoaded: false,
  tokenIsValid: false,
}
const entities = handleActions({
  [LOCATION_CHANGE]: (state, action) => {
    // 起動時にTokenを読み込む
    if(!state.tokenLoaded) {
      CCAPI.setToken(state.token)
      state.token.load()
      return {...state, tokenLoaded: true, tokenIsValid: state.token.isValid()}
    }

    return state
  },

  [actionTypes.auth.loginSucceeded]: (state, action) => {
    let {access_token, refresh_token, scope} = action.payload
    state.token.update(access_token, refresh_token, scope)
    state.token.save()
    let tokenIsValid = state.token.isValid()

    return {...state, tokenIsValid}
  },

}, initialState)
export default entities
