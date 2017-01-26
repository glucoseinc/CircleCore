import {call, fork, put, takeEvery, takeLatest} from 'redux-saga/effects'

import CCAPI from 'src/api'
import actions, {actionTypes} from 'src/actions'
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
 * [updateUser description]
 * @param  {[type]}    action [description]
 */
function* updateUser(action) {
  try {
    const response = yield call(::CCAPI.updateUser, action.payload)
    yield put(actions.user.updateComplete({response}))
  } catch(e) {
    const detail = e.response && e.response.body ? e.response.body.detail : null
    yield put(actions.user.updateComplete({error: makeError(e), detail}))
  }
}


/**
 * [fetchMe description]
 * @param  {[type]}    action [description]
 */
function* fetchMe(action) {
  try {
    const response = yield call(::CCAPI.getMe)
    yield put(actions.users.fetchMeComplete({response}))
  } catch (e) {
    yield put(actions.users.fetchMeComplete({error: makeError(e)}))
  }
}


/**
 * [usersSaga description]
 * @param  {[type]}    args [description]
 */
export default function* usersSaga(...args) {
  yield fork(handleUsersFetchRequest, ...args)
  yield fork(handleUsersDeleteRequest, ...args)

  // user update request
  yield fork(function* () {
    yield takeEvery(actionTypes.user.updateRequest, updateUser)
  })

  // 自分の情報を取得
  yield fork(function* () {
    yield takeEvery(actionTypes.users.fetchMeRequest, fetchMe)
  })
}
