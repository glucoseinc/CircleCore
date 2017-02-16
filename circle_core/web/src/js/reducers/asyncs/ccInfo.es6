import {actionTypes} from 'src/actions'

import {changeFlagAction} from './utils'


const ccInfoActionsHandler = {
  // Fetch myself
  [actionTypes.ccInfo.fetchMyselfRequest]: changeFlagAction('isCcInfoFetching', true),
  [actionTypes.ccInfo.fetchMyselfSucceeded]: changeFlagAction('isCcInfoFetching', false),
  [actionTypes.ccInfo.fetchMyselfFailed]: changeFlagAction('isCcInfoFetching', false),
}

export default ccInfoActionsHandler
