import {fork, put, select, takeEvery} from 'redux-saga/effects'
import {routerActions, LOCATION_CHANGE} from 'react-router-redux'

import actions, {actionTypes} from '../actions'
import {urls} from '../routes'
import * as selectors from '../selectors'


const pathnames = Object.entries(urls).reduce((_pathnames, [key, url]) => ({
  ..._pathnames,
  [key]: url.fullPath,
}), {})


/**
 * [locationChangeJudge description]
 * @param  {[type]}    action [description]
 */
function* locationChangeJudge(action) {
  const requestedPathname = action.payload
  const currentPathname = yield select(selectors.pathname)
  if (currentPathname !== requestedPathname) {
    yield put(routerActions.push(requestedPathname))
  } else {
    yield put(actions.location.changeCancel())
  }
}

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
 * [handleLocationChangeRequest description]
 */
function* handleLocationChangeRequest() {
  yield takeEvery(actionTypes.location.changeRequest, locationChangeJudge)
}

/**
 * [handleLocationChangetoSchemas description]
 */
function* handleLocationChangetoSchemas() {
  const triggerActionTypes = [
    actionTypes.schemas.createSucceeded,
    actionTypes.schemas.deleteSucceeded,
  ]
  yield takeEvery(triggerActionTypes, locationChangetoSchemas)
}

/**
 * [handleLocationChangetoModules description]
 */
function* handleLocationChangetoModules() {
  const triggerActionTypes = [
    actionTypes.modules.createSucceeded,
    actionTypes.modules.deleteSucceeded,
  ]
  yield takeEvery(triggerActionTypes, locationChangetoModules)
}

/**
 * [locationSaga description]
 * @param  {[type]}    args [description]
 */
export default function* locationSaga(...args) {
  yield fork(handleLocationChangeRequest, ...args)
  yield fork(handleLocationChangetoSchemas, ...args)
  yield fork(handleLocationChangetoModules, ...args)
}
