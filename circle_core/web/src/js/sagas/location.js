import {routerActions} from 'connected-react-router'
import {fork, put, takeEvery} from 'redux-saga/effects'

import {actionTypes} from 'src/actions'
import {urls} from 'src/routes'


const pathnames = Object.entries(urls).reduce((_pathnames, [key, url]) => ({
  ..._pathnames,
  [key]: url.fullPath,
}), {})


/**
 * Schema一覧へ遷移
 * @param {object} action
 */
function* locationChangetoSchemas(action) {
  yield put(routerActions.push(pathnames.schemas))
}


/**
 * Module一覧へ遷移
 * @param {object} action
 */
function* locationChangetoModules(action) {
  yield put(routerActions.push(pathnames.modules))
}


/**
 * ReplicationLink一覧へ遷移
 * @param {object} action
 */
function* locationChangetoReplicas(action) {
  yield put(routerActions.push(pathnames.replicas))
}

/**
 * Schema一覧への遷移をハンドル
 */
function* handleLocationChangetoSchemas() {
  const triggerActionTypes = [
    actionTypes.schema.createSucceeded,
    actionTypes.schema.deleteSucceeded,
  ]
  yield takeEvery(triggerActionTypes, locationChangetoSchemas)
}


/**
 * Module一覧への遷移をハンドル
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
 * ReplicationLink一覧への遷移をハンドル
 */
function* handleLocationChangetoReplicas() {
  const triggerActionTypes = [
    actionTypes.replicationLink.deleteSucceeded,
  ]
  yield takeEvery(triggerActionTypes, locationChangetoReplicas)
}


/**
 * ReplicationMaster一覧への遷移をハンドル
 */
function* handleLocationChangeToReplicationMasters() {
  const triggerActionTypes = [
    actionTypes.replicationMaster.createSucceeded,
    actionTypes.replicationMaster.deleteSucceeded,
  ]
  yield takeEvery(triggerActionTypes, function* (action) {
    yield put(routerActions.push(pathnames.replicationMasters))
  })
}


/**
 * Loaction Saga
 * @param {any} args
 */
export default function* locationSaga(...args) {
  yield fork(handleLocationChangetoSchemas, ...args)
  yield fork(handleLocationChangetoModules, ...args)
  yield fork(handleLocationChangetoReplicas, ...args)
  yield fork(handleLocationChangeToReplicationMasters, ...args)
}
