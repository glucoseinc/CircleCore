import {call, fork, put, takeLatest} from 'redux-saga/effects'

import CCAPI from '../api'
import actionTypes from '../actions/actionTypes'
import actions from '../actions'

// import User from '../models/User'


// /**
//  * [createModule description]
//  * @param  {[type]}    action [description]
//  */
// function* createModule(action) {
//   const module = Module.fromObject(action.payload)
//   try {
//     const response = yield call(::CCAPI.postModule, module)
//     yield put(actions.modules.createSucceeded(response))
//   } catch (e) {
//     yield put(actions.modules.createFailed(e.message))
//   }
// }

/**
 * [fetchUsers description]
 * @param  {[type]}    action [description]
 */
function* fetchUsers(action) {
  try {
    const users = yield call(::CCAPI.getUsers)
    yield put(actions.modules.fetchSucceeded(users))
  } catch (e) {
    yield put(actions.modules.fetchFailed(e.message))
  }
}

// /**
//  * [deleteModule description]
//  * @param  {[type]}    action [description]
//  */
// function* deleteModule(action) {
//   const module = Module.fromObject(action.payload)
//   try {
//     const response = yield call(::CCAPI.deleteModule, module)
//     yield put(actions.modules.deleteSucceeded(response))
//   } catch (e) {
//     yield put(actions.modules.deleteFailed(e.message))
//   }
// }


// /**
//  * [handleModulesCreateRequest description]
//  */
// function* handleModulesCreateRequest() {
//   yield takeEvery(actionTypes.modules.createRequest, createModule)
// }

/**
 * [handleUsersFetchRequest description]
 */
function* handleUsersFetchRequest() {
  const triggerActionTypes = [
    actionTypes.users.fetchRequest,
    actionTypes.users.createSucceeded,
    actionTypes.users.deleteSucceeded,
  ]
  yield takeLatest(triggerActionTypes, fetchUsers)
}

// /**
//  * [handleModulesDeleteRequest description]
//  */
// function* handleModulesDeleteRequest() {
//   yield takeEvery(actionTypes.modules.deleteRequest, deleteModule)
// }


/**
 * [usersSaga description]
 * @param  {[type]}    args [description]
 */
export default function* usersSaga(...args) {
  // yield fork(handleModulesCreateRequest, ...args)
  yield fork(handleUsersFetchRequest, ...args)
  // yield fork(handleModulesDeleteRequest, ...args)
}
