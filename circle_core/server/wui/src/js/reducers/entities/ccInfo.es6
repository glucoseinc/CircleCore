import {actionTypes} from 'src/actions'

import {getNewEntities} from './utils'


const mergeCcInfos = (state, action) => {
  const {
    ccInfos,
  } = getNewEntities(action.payload)
  return {
    ...state,
    ccInfos: state.ccInfos.merge(ccInfos),
  }
}

const refreshCcInfos = (state, action) => {
  const {
    ccInfos,
  } = getNewEntities(action.payload)
  return {
    ...state,
    ccInfos,
  }
}

const ccInfoActionsHandler = {
  // Fetch all
  [actionTypes.ccInfo.fetchAllSucceeded]: refreshCcInfos,

  // Fetch myself
  [actionTypes.ccInfo.fetchMyselfSucceeded]: mergeCcInfos,

  // Update
  [actionTypes.ccInfo.updateSucceeded]: mergeCcInfos,
}

export default ccInfoActionsHandler
