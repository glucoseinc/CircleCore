import {fork} from 'redux-saga/effects'
import async from './async'
import auth from './auth'
import errorDialog from './errorDialog'
import location from './location'
import snackbar from './snackbar'


/**
 * rootSaga
 */
export default function* rootSaga() {
  yield fork(async)
  yield fork(auth)
  yield fork(errorDialog)
  yield fork(location)
  yield fork(snackbar)
}
