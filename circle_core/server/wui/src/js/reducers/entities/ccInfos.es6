import {actionTypes} from 'src/actions'

import {getNewEntities} from './utils'


const mergeByFetchingCcInfos = (refresh) => (state, action) => {
  const newEntities = getNewEntities(action.payload)
  return {
    ...state,
    ccInfos: refresh ? newEntities.ccInfos : state.ccInfos.merge(newEntities.ccInfos),
  }
}

const ccInfosActionsHandler = {
  // Fetch
  [actionTypes.ccInfos.fetchSucceeded]: mergeByFetchingCcInfos(true),
  [actionTypes.ccInfos.fetchMyselfSucceeded]: mergeByFetchingCcInfos(false),

  // Update
  [actionTypes.ccInfos.updateSucceeded]: mergeByFetchingCcInfos(false),
}

export default ccInfosActionsHandler
