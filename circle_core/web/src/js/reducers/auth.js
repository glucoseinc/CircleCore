import {handleActions} from 'redux-actions'
import {LOCATION_CHANGE} from 'react-router-redux'

import {actionTypes} from 'src/actions'
import CCAPI from 'src/api'
import {oauthToken} from 'src/Authorization'

const initialState = {
  token: oauthToken,
  tokenLoaded: false,
  tokenIsValid: false,
}
const entities = handleActions({
  [LOCATION_CHANGE]: (state, action) => {
    // 起動時にTokenを読み込む
    if (!state.tokenLoaded) {
      CCAPI.setToken(state.token)
      state.token.load()
      return {...state, tokenLoaded: true, tokenIsValid: state.token.isValid()}
    }

    return state
  },

  [actionTypes.auth.loginSucceeded]: (state, action) => {
    // eslint-disable-next-line camelcase
    const {access_token, refresh_token, scope} = action.payload
    state.token.update(access_token, refresh_token, scope)
    state.token.save()
    const tokenIsValid = state.token.isValid()

    return {...state, tokenIsValid}
  },

  [actionTypes.auth.tokenInvalidated]: (state, action) => {
    state.token.clear()
    return {...state, tokenIsValid: false}
  },

}, initialState)
export default entities
