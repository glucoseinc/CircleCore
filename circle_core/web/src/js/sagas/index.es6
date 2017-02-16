import {fork} from 'redux-saga/effects'
import async from './async'
import auth from './auth'
import error from './error'
import location from './location'
import snackbar from './snackbar'


/**
 * rootSaga
 */
export default function* rootSaga() {
  yield fork(async)
  yield fork(auth)
  yield fork(error)
  yield fork(location)
  yield fork(snackbar)
}
