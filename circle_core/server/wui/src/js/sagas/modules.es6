import {call, fork, put, takeEvery} from 'redux-saga/effects'

import CCAPI from '../api'
import actionTypes from '../constants/ActionTypes'


/**
 * [fetchModules description]
 * @param  {[type]}    action [description]
 */
function* fetchModules(action) {
  try {
    const modules = yield call(::CCAPI.getModules)
    yield put({type: actionTypes.modules.fetchSucceeded, modules: modules})
  } catch (e) {
    yield put({type: actionTypes.modules.fetchFailed, message: e.message})
  }
}

/**
 * [handleModulesFetchRequest description]
 */
function* handleModulesFetchRequest() {
  yield takeEvery(actionTypes.modules.fetchRequested, fetchModules)
}

/**
 * [deleteModule description]
 * @param  {[type]}    action [description]
 */
function* deleteModule(action) {
  try {
    const response = yield call(::CCAPI.deleteModule, action.module.uuid)
    yield put({type: actionTypes.module.deleteSucceeded, response: response})
  } catch (e) {
    yield put({type: actionTypes.module.deleteSucceeded, message: e.message})
  }
}

/**
 * [handleModuleDeleteRequest description]
 */
function* handleModuleDeleteRequest() {
  yield takeEvery(actionTypes.module.deleteRequested, deleteModule)
}

/**
 * [createModule description]
 * @param  {[type]}    action [description]
 */
function* createModule(action) {
  try {
    const response = yield call(::CCAPI.postModule, action.module)
    yield put({type: actionTypes.module.createSucceeded, response: response})
  } catch (e) {
    yield put({type: actionTypes.module.createFailed, message: e.message})
  }
}

/**
 * [handleModuleCreateRequest description]
 */
function* handleModuleCreateRequest() {
  yield takeEvery(actionTypes.module.createRequested, createModule)
}


/**
 * [modulesSaga description]
 * @param  {[type]}    args [description]
 */
export default function* modulesSaga(...args) {
  yield fork(handleModulesFetchRequest, ...args)
  yield fork(handleModuleCreateRequest, ...args)
  yield fork(handleModuleDeleteRequest, ...args)
}
