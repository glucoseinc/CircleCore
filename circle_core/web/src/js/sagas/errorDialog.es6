import {fork, put, takeEvery} from 'redux-saga/effects'

import actions, {actionTypes, actionTypePrefix} from 'src/actions'


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
 * CRUD失敗時
 */
function* handleCrudFailed() {
  const arrayedActionTypes = Object.values(actionTypes).reduce(
    (arrayed, childActionTypes) => [
      ...arrayed,
      ...Object.values(childActionTypes),
    ], []
  )
  const re = new RegExp(`${actionTypePrefix}.*(CREATE|FETCH|UPDATE|DELETE).*FAILED$`)
  const triggerActionTypes = arrayedActionTypes.filter((actionType) => actionType.match(re))
  yield takeEvery(triggerActionTypes, showErrorDialog)
}

/**
 * ErrorDialog Saga
 * @param {any} args
 */
export default function* errorDialogSaga(...args) {
  yield fork(handleCrudFailed, ...args)
}
