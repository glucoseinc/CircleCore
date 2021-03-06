import {handleActions} from 'redux-actions'

import {actionTypes} from 'src/actions'
import CCAPI from 'src/api'
import {oauthToken} from 'src/Authorization'

CCAPI.setToken(oauthToken)
oauthToken.load()

const initialState = {
  token: oauthToken,
  tokenIsValid: oauthToken.isValid(),
}
const entities = handleActions({
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
