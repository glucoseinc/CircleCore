import {actionTypes} from 'src/actions'

import {getNewEntities} from './utils'


const mergeReplicationMasters = (state, action) => {
  const {
    replicationMasters,
  } = getNewEntities(action.payload)
  return {
    ...state,
    replicationMasters: state.replicationMasters.merge(replicationMasters),
  }
}

const refreshReplicationMasters = (state, action) => {
  const {
    replicationMasters,
  } = getNewEntities(action.payload)
  return {
    ...state,
    replicationMasters,
  }
}

const deleteReplicationMasters = (state, action) => {
  const {
    replicationMasters,
  } = getNewEntities(action.payload)
  return {
    ...state,
    replicationMasters: state.replicationMasters.filterNot((obj, objId) =>
      replicationMasters.keySeq().includes(objId)
    ),
  }
}


const replicationLinksActionsHandler = {
  // Create
  [actionTypes.replicationMaster.createSucceeded]: mergeReplicationMasters,

  // Fetch all
  [actionTypes.replicationMaster.fetchAllSucceeded]: refreshReplicationMasters,

  // Delete
  [actionTypes.replicationMaster.deleteSucceeded]: deleteReplicationMasters,
}

export default replicationLinksActionsHandler
