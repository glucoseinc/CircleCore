import {call, fork, put, takeEvery, takeLatest} from 'redux-saga/effects'

import CCAPI from '../api'
import actionTypes from '../actions/actionTypes'
import actions from '../actions'

import Module from '../models/Module'


/**
 * [createModule description]
 * @param  {[type]}    action [description]
 */
function* createModule(action) {
  const module = Module.fromObject(action.payload)
  try {
    const response = yield call(::CCAPI.postModule, module)
    yield put(actions.modules.createSucceeded(response))
  } catch (e) {
    yield put(actions.modules.createFailed(e.message))
  }
}

/**
 * [fetchModules description]
 * @param  {[type]}    action [description]
 */
function* fetchModules(action) {
  try {
    const response = yield call(::CCAPI.getModules)
    yield put(actions.modules.fetchSucceeded(response))
  } catch (e) {
    yield put(actions.modules.fetchFailed(e.message))
  }
}


/**
 * [updateModule description]
 * @param  {[type]}    action [description]
 */
function* updateModule(action) {
  const module = Module.fromObject(action.payload)
  try {
    const response = yield call(::CCAPI.putModule, module)
    yield put(actions.modules.updateSucceeded(response))
  } catch (e) {
    yield put(actions.modules.updateFailed(e.message))
  }
}


/**
 * [deleteModule description]
 * @param  {[type]}    action [description]
 */
function* deleteModule(action) {
  const module = Module.fromObject(action.payload)
  try {
    const response = yield call(::CCAPI.deleteModule, module)
    yield put(actions.modules.deleteSucceeded(response))
  } catch (e) {
    yield put(actions.modules.deleteFailed(e.message))
  }
}


/**
 * [handleModulesCreateRequest description]
 */
function* handleModulesCreateRequest() {
  yield takeEvery(actionTypes.modules.createRequest, createModule)
}

/**
 * [handleModulesFetchRequest description]
 */
function* handleModulesFetchRequest() {
  const triggerActionTypes = [
    actionTypes.modules.fetchRequest,
    actionTypes.modules.createSucceeded,
    actionTypes.modules.updateSucceeded,
    actionTypes.modules.deleteSucceeded,
  ]
  yield takeLatest(triggerActionTypes, fetchModules)
}

/**
   * [handleModulesUpdateRequest description]
 */
function* handleModulesUpdateRequest() {
  yield takeLatest(actionTypes.modules.updateRequest, updateModule)
}

/**
 * [handleModulesDeleteRequest description]
 */
function* handleModulesDeleteRequest() {
  yield takeEvery(actionTypes.modules.deleteRequest, deleteModule)
}


/**
 * [modulesSaga description]
 * @param  {[type]}    args [description]
 */
export default function* modulesSaga(...args) {
  yield fork(handleModulesCreateRequest, ...args)
  yield fork(handleModulesFetchRequest, ...args)
  yield fork(handleModulesUpdateRequest, ...args)
  yield fork(handleModulesDeleteRequest, ...args)
}
