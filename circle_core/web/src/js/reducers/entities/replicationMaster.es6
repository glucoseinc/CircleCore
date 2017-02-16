import {actionTypes} from 'src/actions'

import {getNewEntities} from './utils'


// const mergeReplicationLinks = (state, action) => {
//   const {
//     replicationLinks,
//     ccInfos,
//     modules,
//     schemas,
//   } = getNewEntities(action.payload)
//   return {
//     ...state,
//     replicationLinks: state.replicationLinks.merge(replicationLinks),
//     ccInfos: state.ccInfos.merge(ccInfos),
//     modules: state.modules.merge(modules),
//     schemas: state.schemas.merge(schemas),
//   }
// }

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
  // // Create
  // [actionTypes.replicationLink.createSucceeded]: mergeReplicationLinks,

  // Fetch all
  [actionTypes.replicationMaster.fetchAllSucceeded]: refreshReplicationMasters,

  // Delete
  [actionTypes.replicationMaster.deleteSucceeded]: deleteReplicationMasters,
}

export default replicationLinksActionsHandler
