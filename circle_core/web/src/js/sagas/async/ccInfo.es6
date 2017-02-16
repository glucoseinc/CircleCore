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
}

export default asyncSagaParams
