import {fork} from 'redux-saga/effects'
import auth from './auth'
import async from './async'
import invitations from './invitations'
import location from './location'
import users from './users'


/**
 * rootSaga
 */
export default function* rootSaga() {
  yield fork(auth)
  yield fork(async)
  yield fork(invitations)
  yield fork(location)
  yield fork(users)
}
