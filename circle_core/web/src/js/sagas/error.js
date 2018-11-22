import {fork, put, takeEvery} from 'redux-saga/effects'

import actions, {actionTypes, actionTypePrefix} from 'src/actions'


/**
 * User Update失敗時の動作
 * @param {object} action
 */
function* onUserUpdateFailed(action) {
  yield put(actions.error.onUserUpdate(action.payload.errors))
}

/**
 * User Update Failed
 */
function* handleUserUpdateFailed() {
  yield takeEvery([actionTypes.user.updateFailed], onUserUpdateFailed)
}


/**
 * ErrorDialog を表示する
 * @param {object} action
 */
function* showErrorDialog(action) {
  let payload = {
    actionType: action.type,
  }
  if (typeof action.payload === 'string') {
    payload = {
      ...payload,
      message: action.payload,
    }
  } else if (typeof action.payload === 'object') {
    payload = {
      ...payload,
      ...action.payload,
    }
  }
  yield put(actions.page.showErrorDialog(payload))
}

/**
 * その他のCRUD失敗時
 */
function* handleCrudFailed() {
  const ignoredActionTypes = [
    actionTypes.user.updateFailed,
  ]
  const arrayedActionTypes = Object.values(actionTypes).reduce(
    (arrayed, childActionTypes) => [
      ...arrayed,
      ...Object.values(childActionTypes),
    ], []
  )
  const re = new RegExp(`${actionTypePrefix}.*(CREATE|FETCH|UPDATE|DELETE).*FAILED$`)
  const triggerActionTypes = arrayedActionTypes.filter(
    (actionType) => actionType.match(re)
  ).filter(
    (actionType) => !ignoredActionTypes.includes(actionType)
  )
  yield takeEvery(triggerActionTypes, showErrorDialog)
}


/**
 * Error Saga
 * @param {any} args
 */
export default function* errorSaga(...args) {
  yield fork(handleUserUpdateFailed, ...args)
  yield fork(handleCrudFailed, ...args)
}
