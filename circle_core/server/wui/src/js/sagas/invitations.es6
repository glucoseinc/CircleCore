import {call, fork, put, takeEvery} from 'redux-saga/effects'

import CCAPI from 'src/api'
import actions, {actionTypes} from 'src/actions'
import {makeError} from './utils'

/**
 * [fetchInvitations description]
 * @param  {[type]}    action [description]
 */
function* fetchInvitations(action) {
  try {
    const response = yield call(::CCAPI.listInvitations, action.payload)
    yield put(actions.invitations.fetchComplete({response}))
  } catch (e) {
    yield put(actions.invitations.fetchComplete({error: makeError(e)}))
  }
}


/**
 * [createInvitation description]
 * @param  {[type]}    action [description]
 */
function* createInvitation(action) {
  try {
    const response = yield call(::CCAPI.postInvitation, action.payload)
    yield put(actions.invitations.createComplete({response}))
  } catch (e) {
    yield put(actions.invitations.createComplete({error: makeError(e)}))
  }
}

/**
 * [deleteInvitation description]
 * @param  {[type]}    action [description]
 */
function* deleteInvitation(action) {
  try {
    const response = yield call(::CCAPI.deleteInvitation, action.payload)
    yield put(actions.invitations.deleteComplete({response}))
  } catch (e) {
    yield put(actions.invitations.deleteComplete({error: makeError(e)}))
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
