import {call, fork, put, takeEvery} from 'redux-saga/effects'

import CCAPI from '../api'
import actions, {actionTypes} from '../actions'
import Schema from '../models/Schema'


/**
 * [fetchSchema description]
 * @param  {[type]}    action [description]
 */
function* fetchSchema(action) {
  const schema = Schema.fromObject({
    uuid: action.payload,
  })

  try {
    const response = yield call(::CCAPI.getSchema, schema)
    yield put(actions.schema.fetchSucceeded(response))
  } catch (e) {
    yield put(actions.schema.fetchFailed(e.message))
  }
}


/**
 * [handleSchemaFetchRequest description]
 */
function* handleSchemaFetchRequest() {
  const triggerActionTypes = [
    actionTypes.schema.fetchRequest,
  ]
  yield takeEvery(triggerActionTypes, fetchSchema)
}


/**
 * [schemaSaga description]
 * @param  {[type]}    args [description]
 */
export default function* schemasSaga(...args) {
  yield fork(handleSchemaFetchRequest, ...args)
}
