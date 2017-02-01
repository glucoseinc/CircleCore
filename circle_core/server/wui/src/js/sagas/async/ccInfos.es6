import CCAPI from 'src/api'
import actions, {actionTypes} from 'src/actions'

import {createAsyncSagaParam} from './utils'


// Read myself
const myselfCcInfoFetchParam = createAsyncSagaParam(
  ::CCAPI.fetchMyselfCcInfo,
  () => null,
  actions.ccInfos.fetchMyselfSucceeded,
  actions.ccInfos.fetchMyselfFailed
)

// Read all
const allCcInfosFetchParam = createAsyncSagaParam(
  ::CCAPI.fetchAllCcInfos,
  () => null,
  actions.ccInfos.fetchSucceeded,
  actions.ccInfos.fetchFailed
)

const asyncSagaParams = {
  // Read myself
  [actionTypes.ccInfos.fetchMyselfRequest]: myselfCcInfoFetchParam,

  // Read all
  [actionTypes.ccInfos.fetchRequest]: allCcInfosFetchParam,
}

export default asyncSagaParams
