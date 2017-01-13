import {fork, put, takeEvery} from 'redux-saga/effects'

import actionTypes from '../actions/actionTypes'
import actions from '../actions'

import Module from '../models/Module'


/**
 * [executeModuleEdit description]
 * @param  {[type]}    action [description]
 */
function* executeModuleEdit(action) {
  const module = Module.fromObject(action.payload)
  yield put(actions.modules.updateRequest(module))
}


/**
 * [handleModuleEditExecute description]
 */
function* handleModuleEditExecute() {
  yield takeEvery(actionTypes.misc.executeModuleEdit, executeModuleEdit)
}


/**
 * [miscSaga description]
 * @param  {[type]}    args [description]
 */
export default function* miscSaga(...args) {
  yield fork(handleModuleEditExecute, ...args)
}
