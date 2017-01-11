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
    const modules = yield call(::CCAPI.getModules)
    yield put(actions.modules.fetchSucceeded(modules))
  } catch (e) {
    yield put(actions.modules.fetchFailed(e.message))
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
    actionTypes.modules.deleteSucceeded,
  ]
  yield takeLatest(triggerActionTypes, fetchModules)
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
  yield fork(handleModulesDeleteRequest, ...args)
}
