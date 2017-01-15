import {call, fork, put, takeEvery} from 'redux-saga/effects'

import CCAPI from '../api'
import actions, {actionTypes} from '../actions'


/**
 * 例外オブジェから、Actionの返り値用のErrorを作り直す
 * @param {Error} e
 * @return {Error} new error
 */
function _makeError(e) {
  let msg = (e.response && e.response.body && e.response.body.detail && e.response.body.detail.reason) || e.message
  return new Error(msg)
}


/**
 * [fetchInvitations description]
 * @param  {[type]}    action [description]
 */
function* fetchInvitations(action) {
  try {
    const invitations = yield call(::CCAPI.listInvitations, action.payload)

    yield put(actions.invitations.fetchComplete({invitations}))
  } catch (e) {
    yield put(actions.invitations.fetchComplete({error: _makeError(e)}))
  }
}


/**
 * [createInvitation description]
 * @param  {[type]}    action [description]
 */
function* createInvitation(action) {
  try {
    const invitation = yield call(::CCAPI.postInvitation, action.payload)

    yield put(actions.invitations.createComplete({invitation}))
  } catch (e) {
    yield put(actions.invitations.createComplete({error: _makeError(e)}))
  }
}

/**
 * [deleteInvitation description]
 * @param  {[type]}    action [description]
 */
function* deleteInvitation(action) {
  try {
    const invitation = yield call(::CCAPI.deleteInvitation, action.payload)

    yield put(actions.invitations.deleteComplete({invitation}))
  } catch (e) {
    yield put(actions.invitations.deleteComplete({error: _makeError(e)}))
  }
}


/**
 * [invitationsSaga description]
 * @param  {[type]}    args [description]
 */
export default function* invitationsSaga(...args) {
  // install action watchers
  yield fork(function* () {
    yield takeEvery(actionTypes.invitations.fetchRequest, fetchInvitations)
  })

  yield fork(function* () {
    yield takeEvery(actionTypes.invitations.createRequest, createInvitation)
  })

  yield fork(function* () {
    yield takeEvery(actionTypes.invitations.deleteRequest, deleteInvitation)
  })
}
