import {LOCATION_CHANGE} from 'connected-react-router'
import {call, fork, put, select, takeLatest} from 'redux-saga/effects'

import actions from 'src/actions'
import {checkHasAuthCodeReceived, fetchTokenByAuthorizationCode} from 'src/Authorization'


/**
 * [checkAuthorizationHash description]
 * @param  {[type]}    action [description]
 */
function* checkAuthorizationHash({payload: {hash}}) {
  const authCode = checkHasAuthCodeReceived(hash)

  if (!authCode) {
    return
  }

  const auth = yield select((state) => state.auth)

  if (auth.tokenIsValid) {
    // 認証済みだったらAuthCodeは無視
    return
  }

  const tokenData = yield call(fetchTokenByAuthorizationCode, authCode)

  if (tokenData) {
    yield put(actions.auth.loginSucceeded(tokenData))
  } else {
    yield put(actions.auth.loginFailed(tokenData))
  }
}


/**
 * [invitationsSaga description]
 * @param  {[type]}    args [description]
 */
export default function* invitationsSaga(...args) {
  yield fork(function* () {
    yield takeLatest(LOCATION_CHANGE, checkAuthorizationHash)
  })
}
