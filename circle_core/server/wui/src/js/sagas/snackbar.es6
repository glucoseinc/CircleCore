import {fork, put, takeEvery} from 'redux-saga/effects'

import actions, {actionTypes} from 'src/actions'


const messages = {
  [actionTypes.user.updateSucceeded]: '保存しました',
}

/**
 * Snackbar を表示する
 * @param {object} action
 */
function* showSnackbar(action) {
  yield put(actions.page.showSnackbar(messages[action.type]))
}

/**
 * Snackbar表示Saga
 */
function* handleShowSnackbar() {
  const triggerActionTypes = Object.keys(messages)
  yield takeEvery(triggerActionTypes, showSnackbar)
}

/**
 * Snackbar Saga
 * @param {any} args
 */
export default function* snackbarSaga(...args) {
  yield fork(handleShowSnackbar, ...args)
}
