import {call, fork, put, takeEvery, takeLatest} from 'redux-saga/effects'

import CCAPI from '../api'
import actionTypes from '../actions/actionTypes'
import actions from '../actions'

import Schema from '../models/Schema'


/**
 * [createSchema description]
 * @param  {[type]}    action [description]
 */
function* createSchema(action) {
  const schema = Schema.fromObject(action.payload)
  try {
    const response = yield call(::CCAPI.postSchema, schema)
    yield put(actions.schemas.createSucceeded(response))
  } catch (e) {
    yield put(actions.schemas.createFailed(e.message))
  }
}

/**
 * [fetchSchemas description]
 * @param  {[type]}    action [description]
 */
function* fetchSchemas(action) {
  try {
    const schemas = yield call(::CCAPI.getSchemas)
    yield put(actions.schemas.fetchSucceeded(schemas))
  } catch (e) {
    yield put(actions.schemas.fetchFailed(e.message))
  }
}

/**
 * [deleteSchema description]
 * @param  {[type]}    action [description]
 */
function* deleteSchema(action) {
  const schema = Schema.fromObject(action.payload)
  try {
    const response = yield call(::CCAPI.deleteSchema, schema)
    yield put(actions.schemas.deleteSucceeded(response))
  } catch (e) {
    yield put(actions.schemas.deleteFailed(e.message))
  }
}


/**
 * [fetchSchemaPropertyTypes description]
 * @param  {[type]}    action [description]
 */
function* fetchSchemaPropertyTypes(action) {
  try {
    const schemaPropertyTypes = yield call(::CCAPI.getSchemaPropertyTypes)
    yield put(actions.schemaPropertyTypes.fetchSucceeded(schemaPropertyTypes))
  } catch (e) {
    yield put(actions.schemaPropertyTypes.fetchFailed(e.message))
  }
}


/**
 * [handleSchemasCreateRequest description]
 */
function* handleSchemasCreateRequest() {
  yield takeEvery(actionTypes.schemas.createRequest, createSchema)
}

/**
 * [handleSchemasFetchRequest description]
 */
function* handleSchemasFetchRequest() {
  const triggerActionTypes = [
    actionTypes.schemas.fetchRequest,
    actionTypes.schemas.createSucceeded,
    actionTypes.schemas.deleteSucceeded,
  ]
  yield takeLatest(triggerActionTypes, fetchSchemas)
}

/**
 * [handleSchemasDeleteRequest description]
 */
function* handleSchemasDeleteRequest() {
  yield takeEvery(actionTypes.schemas.deleteRequest, deleteSchema)
}


/**
 * [handleSchemaPropertyTypesFetchRequest description]
 */
function* handleSchemaPropertyTypesFetchRequest() {
  yield takeLatest(actionTypes.schemaPropertyTypes.fetchRequest, fetchSchemaPropertyTypes)
}


/**
 * [schemasSaga description]
 * @param  {[type]}    args [description]
 */
export default function* schemasSaga(...args) {
  yield fork(handleSchemasCreateRequest, ...args)
  yield fork(handleSchemasFetchRequest, ...args)
  yield fork(handleSchemasDeleteRequest, ...args)

  yield fork(handleSchemaPropertyTypesFetchRequest, ...args)
}
