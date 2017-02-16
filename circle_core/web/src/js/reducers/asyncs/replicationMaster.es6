import {actionTypes} from 'src/actions'
import {changeFlagAction} from './utils'


const replicationMasterActionsHandler = {
  // Fetch all
  [actionTypes.replicationMaster.fetchAllRequest]: changeFlagAction('isReplicationMasterFetching', true),
  [actionTypes.replicationMaster.fetchAllSucceeded]: changeFlagAction('isReplicationMasterFetching', false),
  [actionTypes.replicationMaster.fetchAllFailed]: changeFlagAction('isReplicationMasterFetching', false),

  // Update
  [actionTypes.replicationMaster.deleteRequest]: changeFlagAction('isReplicationMasterDeleting', true),
  [actionTypes.replicationMaster.deleteSucceeded]: changeFlagAction('isReplicationMasterDeleting', false),
  [actionTypes.replicationMaster.deleteFailed]: changeFlagAction('isReplicationMasterDeleting', false),
}

export default replicationMasterActionsHandler
