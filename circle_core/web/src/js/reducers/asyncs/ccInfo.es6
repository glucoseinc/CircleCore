import {actionTypes} from 'src/actions'

import {changeFlagAction} from './utils'


const ccInfoActionsHandler = {
  // Fetch myself
  [actionTypes.ccInfo.fetchMyselfRequest]: changeFlagAction('isCcInfoFetching', true),
  [actionTypes.ccInfo.fetchMyselfSucceeded]: changeFlagAction('isCcInfoFetching', false),
  [actionTypes.ccInfo.fetchMyselfFailed]: changeFlagAction('isCcInfoFetching', false),

  // Update
  [actionTypes.ccInfo.updateRequest]: changeFlagAction('isCcInfoUpdating', true),
  [actionTypes.ccInfo.updateSucceeded]: changeFlagAction('isCcInfoUpdating', false),
  [actionTypes.ccInfo.updateFailed]: changeFlagAction('isCcInfoUpdating', false),
}

export default ccInfoActionsHandler
