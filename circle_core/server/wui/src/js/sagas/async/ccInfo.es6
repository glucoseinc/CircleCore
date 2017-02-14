import CCAPI from 'src/api'
import actions, {actionTypes} from 'src/actions'

import {createAsyncSagaParam} from './utils'


// Fetch all
const allCcInfosFetchParam = createAsyncSagaParam(
  ::CCAPI.fetchAllCcInfos,
  () => null,
  actions.ccInfo.fetchAllSucceeded,
  actions.ccInfo.fetchAllFailed
)

// Fetch myself
const myselfCcInfoFetchParam = createAsyncSagaParam(
  ::CCAPI.fetchMyselfCcInfo,
  () => null,
  actions.ccInfo.fetchMyselfSucceeded,
  actions.ccInfo.fetchMyselfFailed
)

// Update
const ccInfoUpdateParam = createAsyncSagaParam(
  ::CCAPI.updateCcInfo,
  (payload) => payload,
  actions.ccInfo.updateSucceeded,
  actions.ccInfo.updateFailed
)

const asyncSagaParams = {
  // Fetch all
  [actionTypes.ccInfo.fetchAllRequest]: allCcInfosFetchParam,

  // Fetch myself
  [actionTypes.ccInfo.fetchMyselfRequest]: myselfCcInfoFetchParam,

  // Update
  [actionTypes.ccInfo.updateRequest]: ccInfoUpdateParam,
}

export default asyncSagaParams
