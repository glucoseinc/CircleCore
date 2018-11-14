import CCAPI from 'src/api'
import actions, {actionTypes} from 'src/actions'
import {createAsyncSagaParam} from './utils'


const asyncSagaParams = {
  // Fetch myself
  [actionTypes.ccInfo.fetchMyselfRequest]: createAsyncSagaParam(
    ::CCAPI.fetchMyselfCcInfo,
    () => null,
    actions.ccInfo.fetchMyselfSucceeded,
    actions.ccInfo.fetchMyselfFailed
  ),

  // update
  [actionTypes.ccInfo.updateRequest]: createAsyncSagaParam(
    ::CCAPI.updateCcInfo,
    (payload) => payload,
    actions.ccInfo.updateSucceeded,
    actions.ccInfo.updateFailed
  ),
}

export default asyncSagaParams
