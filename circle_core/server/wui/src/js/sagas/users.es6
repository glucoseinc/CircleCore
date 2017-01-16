import {call, fork, put, takeEvery, takeLatest} from 'redux-saga/effects'

import CCAPI from '../api'
import actions, {actionTypes} from '../actions'
import {makeError} from './utils'


/**
 * [fetchUsers description]
 * @param  {[type]}    action [description]
 */
function* fetchUsers(action) {
  try {
    const response = yield call(::CCAPI.listUsers)
    yield put(actions.users.fetchComplete({response}))
  } catch (e) {
    yield put(actions.users.fetchComplete({error: makeError(e)}))
  }
}


/**
 * [deleteUser description]
 * @param  {[type]}    action [description]
 */
function* deleteUser(action) {
  try {
    const response = yield call(::CCAPI.deleteUser, action.payload)
    yield put(actions.users.deleteComplete({response}))
  } catch (e) {
    yield put(actions.users.deleteComplete({error: makeError(e)}))
  }
}

// handlers
/**
 * [handleUsersFetchRequest description]
 */
function* handleUsersFetchRequest() {
  const triggerActionTypes = [
    actionTypes.users.fetchRequest,
    actionTypes.users.deleteComplete,
  ]
  yield takeLatest(triggerActionTypes, fetchUsers)
}

/**
 * [handleUserssDeleteRequest description]
 */
function* handleUsersDeleteRequest() {
  yield takeEvery(actionTypes.users.deleteRequest, deleteUser)
}


/**
 * [usersSaga description]
 * @param  {[type]}    args [description]
 */
export default function* usersSaga(...args) {
  yield fork(handleUsersFetchRequest, ...args)
  yield fork(handleUsersDeleteRequest, ...args)
}
