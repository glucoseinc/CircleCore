import {actionTypes} from 'src/actions'

import {changeFlagAction} from './utils'


const replicationLinksActionsHandler = {
  // Create
  [actionTypes.replicationLink.createRequest]: changeFlagAction('isReplicationLinkCreating', true),
  [actionTypes.replicationLink.createSucceeded]: changeFlagAction('isReplicationLinkCreating', false),
  [actionTypes.replicationLink.createFailed]: changeFlagAction('isReplicationLinkCreating', false),

  // Fetch all
  [actionTypes.replicationLink.fetchAllRequest]: changeFlagAction('isReplicationLinkFetching', true),
  [actionTypes.replicationLink.fetchAllSucceeded]: changeFlagAction('isReplicationLinkFetching', false),
  [actionTypes.replicationLink.fetchAllFailed]: changeFlagAction('isReplicationLinkFetching', false),
}

export default replicationLinksActionsHandler
