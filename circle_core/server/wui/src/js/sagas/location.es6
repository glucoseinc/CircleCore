import {fork, put, select, takeEvery} from 'redux-saga/effects'
import {matchPattern} from 'react-router/lib/PatternUtils'
import {routerActions} from 'react-router-redux'

import actionTypes from '../constants/ActionTypes'
import {urls} from '../routes'
import * as selector from '../selectors'

const pathnames = (() => {
  let _pathnames = {}
  Object.entries(urls).forEach(([key, url]) => {
    _pathnames[key] = url.fullPath
  })
  return _pathnames
})()

/**
 * [matched description]
 * @param  {[type]} pattern  [description]
 * @param  {[type]} pathname [description]
 * @return {[type]}          [description]
 */
function matched(pattern, pathname) {
  if (Object.values(pathnames).filter((_pathname) => _pathname === pathname).length !== 0) {
    return false
  }
  return matchPattern(pattern, pathname) !== null
}

/**
 * [onLocationChange description]
 * @param  {[type]}    action [description]
 */
function* onLocationChange(action) {
  const pathname = action.payload.pathname
  switch (pathname) {
  case pathnames.schemas:
    yield put({type: actionTypes.schemas.fetchRequested})
    break
  case pathnames.schemasNew:
    yield put({type: actionTypes.schema.createInit})
    yield put({type: actionTypes.schema.propertyTypes.fetchRequested})
    break
  case pathnames.modules:
    yield put({type: actionTypes.modules.fetchRequested})
    break
  default: {
    if (matched(pathnames.schema, pathname)) {
      yield put({type: actionTypes.schemas.fetchRequested})
    }
    yield
  }
  }
}

/**
 * [handleLocationChangeExecuted description]
 */
function* handleLocationChangeExecuted() {
  yield takeEvery(actionTypes.location.change, onLocationChange)
}

/**
 * [locationChangeJudge description]
 * @param  {[type]}    action [description]
 */
function* locationChangeJudge(action) {
  const currentPathname = yield select(selector.pathname)
  if (currentPathname !== action.pathname) {
    yield put(routerActions.push(action.pathname))
  } else {
    yield put({type: actionTypes.location.changeCanceled})
  }
}

/**
 * [handleLocationChangeRequet description]
 */
function* handleLocationChangeRequet() {
  yield takeEvery(actionTypes.location.changeRequested, locationChangeJudge)
}


/**
 * [locationChangetoSchemas description]
 * @param  {[type]}    action [description]
 */
function* locationChangetoSchemas(action) {
  yield put(routerActions.push(pathnames.schemas))
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
 * [locationSaga description]
 * @param  {[type]}    args [description]
 */
export default function* locationSaga(...args) {
  yield fork(handleLocationChangeExecuted, ...args)
  yield fork(handleLocationChangeRequet, ...args)
  yield fork(handleLocationChangetoSchemas, ...args)
}
