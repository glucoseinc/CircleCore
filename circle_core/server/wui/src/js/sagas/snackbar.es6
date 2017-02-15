import {fork, put, takeEvery} from 'redux-saga/effects'

import actions, {actionTypes, actionTypePrefix} from 'src/actions'


/**
 * Snackbar を表示する
 * @param {object} action
 */
function* showSnackbar(action) {
  const message = action.type.includes('CREATE') ? '作成しました' :
    action.type.includes('UPDATE') ? '更新しました' :
    /* action.type.includes('DELETE') ? */ '削除しました'

  yield put(actions.page.showSnackbar(message))
}

/**
 * CRUD成功時
 */
function* handleCrudSucceeded() {
  const arrayedActionTypes = Object.values(actionTypes).reduce(
    (arrayed, childActionTypes) => [
      ...arrayed,
      ...Object.values(childActionTypes),
    ], []
  )
  const re = new RegExp(`${actionTypePrefix}.*(CREATE|UPDATE|DELETE).*SUCCEEDED$`)
  const triggerActionTypes = arrayedActionTypes.filter((actionType) => actionType.match(re))
  yield takeEvery(triggerActionTypes, showSnackbar)
}


/**
 * Snackbar Saga
 * @param {any} args
 */
export default function* snackbarSaga(...args) {
  yield fork(handleCrudSucceeded, ...args)
}
