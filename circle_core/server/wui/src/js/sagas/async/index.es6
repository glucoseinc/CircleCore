import {call, fork, put, takeEvery} from 'redux-saga/effects'

import asyncCcInfoSagaParams from './ccInfo'
import asyncModuleSagaParams from './module'
import asyncReplicationLinkSagaParams from './replicationLink'
import asyncSchemaSagaParams from './schema'
import asyncSchemaPropertyTypeSaga from './schemaPropertyType'
import asyncUserSagaParams from './user'


const asyncSagaParams = {
  ...asyncCcInfoSagaParams,
  ...asyncModuleSagaParams,
  ...asyncReplicationLinkSagaParams,
  ...asyncSchemaSagaParams,
  ...asyncSchemaPropertyTypeSaga,
  ...asyncUserSagaParams,
}

const triggerActionTypes = Object.keys(asyncSagaParams)

/**
 * [crudRequest]
 * @param  {object} action
 */
function* crudRequest(action) {
  const {
    api,
    apiParam,
    succeededAction,
    failedAction,
  } = asyncSagaParams[action.type]

  try {
    const response = yield call(api, apiParam(action.payload))
    yield put(succeededAction(response))
  } catch (e) {
    yield put(failedAction(e.message))
  }
}


/**
 * [handleCrudRequest]
 */
function* handleCrudRequest() {
  yield takeEvery(triggerActionTypes, crudRequest)
}


/**
 * [asyncSaga]
 * @param  {*} args
 */
export default function* asyncSaga(...args) {
  yield fork(handleCrudRequest, ...args)
}
