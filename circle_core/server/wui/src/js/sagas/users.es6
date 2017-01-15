import {call, fork, put, takeEvery, takeLatest} from 'redux-saga/effects'

import CCAPI from '../api'
import actions, {actionTypes} from '../actions'
import User from '../models/User'


/**
 * [fetchUsers description]
 * @param  {[type]}    action [description]
 */
function* fetchUsers(action) {
  try {
    const users = yield call(::CCAPI.getUsers)
    yield put(actions.users.fetchSucceeded(users))
  } catch (e) {
    yield put(actions.users.fetchFailed(e.message))
  }
}


/**
 * [deleteUser description]
 * @param  {[type]}    action [description]
 */
function* deleteUser(action) {
  const user = User.fromObject(action.payload)

  try {
    const response = yield call(::CCAPI.deleteUser, user)
    yield put(actions.users.deleteComplete(response))
  } catch (e) {
    yield put(actions.users.deleteComplete(new Error(e.response.body.detail.reason || e.message)))
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
