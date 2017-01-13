import {call, fork, put, takeEvery} from 'redux-saga/effects'

import CCAPI from '../api'
import actionTypes from '../actions/actionTypes'
import actions from '../actions'

import Module from '../models/Module'


/**
 * [fetchModule description]
 * @param  {[type]}    action [description]
 */
function* fetchModule(action) {
  const module = Module.fromObject({
    uuid: action.payload,
  })

  try {
    const response = yield call(::CCAPI.getModule, module)
    yield put(actions.module.fetchSucceeded(response))
  } catch (e) {
    yield put(actions.module.fetchFailed(e.message))
  }
}


/**
 * [handleModuleFetchRequest description]
 */
function* handleModuleFetchRequest() {
  const triggerActionTypes = [
    actionTypes.module.fetchRequest,
  ]
  yield takeEvery(triggerActionTypes, fetchModule)
}


/**
 * [moduleSaga description]
 * @param  {[type]}    args [description]
 */
export default function* modulesSaga(...args) {
  yield fork(handleModuleFetchRequest, ...args)
}
