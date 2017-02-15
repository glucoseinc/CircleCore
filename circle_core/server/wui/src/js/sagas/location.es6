import {fork, put, takeEvery} from 'redux-saga/effects'
import {routerActions, LOCATION_CHANGE} from 'react-router-redux'

import {actionTypes} from 'src/actions'
import {urls} from 'src/routes'


const pathnames = Object.entries(urls).reduce((_pathnames, [key, url]) => ({
  ..._pathnames,
  [key]: url.fullPath,
}), {})


/**
 * [locationChangetoSchemas description]
 * @param  {[type]}    action [description]
 */
function* locationChangetoSchemas(action) {
  yield put(routerActions.push(pathnames.schemas))
}

/**
 * [locationChangetoModules description]
 * @param  {[type]}    action [description]
 */
function* locationChangetoModules(action) {
  yield put(routerActions.push(pathnames.modules))
}

/**
 * [handleLocationChangetoSchemas description]
 */
function* handleLocationChangetoSchemas() {
  const triggerActionTypes = [
    actionTypes.schema.createSucceeded,
    actionTypes.schema.deleteSucceeded,
  ]
  yield takeEvery(triggerActionTypes, locationChangetoSchemas)
}

/**
 * [handleLocationChangetoModules description]
 */
function* handleLocationChangetoModules() {
  const triggerActionTypes = [
    actionTypes.module.createSucceeded,
    actionTypes.module.deleteSucceeded,
    actionTypes.replicationLink.createSucceeded,
  ]
  yield takeEvery(triggerActionTypes, locationChangetoModules)
}

/**
 * [locationSaga description]
 * @param  {[type]}    args [description]
 */
export default function* locationSaga(...args) {
  yield fork(handleLocationChangetoSchemas, ...args)
  yield fork(handleLocationChangetoModules, ...args)
}
