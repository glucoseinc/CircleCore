import {call, fork, put, takeEvery, takeLatest} from 'redux-saga/effects'

import CCAPI from '../api'
import actionTypes from '../constants/ActionTypes'


/**
 * [fetchSchemas description]
 * @param  {[type]}    action [description]
 */
function* fetchSchemas(action) {
  try {
    const schemas = yield call(::CCAPI.getSchemas)
    yield put({type: actionTypes.schemas.fetchSucceeded, schemas: schemas})
  } catch (e) {
    yield put({type: actionTypes.schemas.fetchFailed, message: e.message})
  }
}

/**
 * [handleSchemasFetchRequest description]
 */
function* handleSchemasFetchRequest() {
  yield takeEvery(actionTypes.schemas.fetchRequested, fetchSchemas)
}

/**
 * [deleteSchema description]
 * @param  {[type]}    action [description]
 */
function* deleteSchema(action) {
  try {
    const response = yield call(::CCAPI.deleteSchema, action.schema.uuid)
    yield put({type: actionTypes.schema.deleteSucceeded, response: response})
  } catch (e) {
    yield put({type: actionTypes.schema.deleteFailed, message: e.message})
  }
}

/**
 * [handleSchemaDeleteRequest description]
 */
function* handleSchemaDeleteRequest() {
  yield takeEvery(actionTypes.schema.deleteRequested, deleteSchema)
}

/**
 * [createSchema description]
 * @param  {[type]}    action [description]
 */
function* createSchema(action) {
  try {
    const response = yield call(::CCAPI.postSchema, action.schema)
    yield put({type: actionTypes.schema.createSucceeded, response: response})
  } catch (e) {
    yield put({type: actionTypes.schema.createFailed, message: e.message})
  }
}

/**
 * [handleSchemaCreateRequest description]
 */
function* handleSchemaCreateRequest() {
  yield takeEvery(actionTypes.schema.createRequested, createSchema)
}


/**
 * [fetchSchemaPropertyTypes description]
 * @param  {[type]}    action [description]
 */
function* fetchSchemaPropertyTypes(action) {
  try {
    const schemaPropertyTypes = yield call(::CCAPI.getSchemaPropertyTypes)
    yield put({type: actionTypes.schema.propertyTypes.fetchSucceeded, schemaPropertyTypes: schemaPropertyTypes})
  } catch (e) {
    yield put({type: actionTypes.schema.propertyTypes.fetchFailed, message: e.message})
  }
}

/**
 * [handleSchemaPropertyTypeFetchRequest description]
 */
function* handleSchemaPropertyTypeFetchRequest() {
  yield takeLatest(actionTypes.schema.propertyTypes.fetchRequested, fetchSchemaPropertyTypes)
}


/**
 * [schemasSaga description]
 * @param  {[type]}    args [description]
 */
export default function* schemasSaga(...args) {
  yield fork(handleSchemasFetchRequest, ...args)
  yield fork(handleSchemaCreateRequest, ...args)
  yield fork(handleSchemaDeleteRequest, ...args)
  yield fork(handleSchemaPropertyTypeFetchRequest, ...args)
}
