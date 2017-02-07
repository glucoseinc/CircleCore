import {actionTypes} from 'src/actions'

import {getNewEntities} from './utils'


const mergeByFetchingReplicationLinks = (refresh) => (state, action) => {
  const newEntities = getNewEntities(action.payload)
  return {
    ...state,
    ccInfos: refresh ? newEntities.ccInfos : state.ccInfos.merge(newEntities.ccInfos),
    schemas: state.schemas.merge(newEntities.schemas),
    modules: refresh ? newEntities.modules : state.modules.merge(newEntities.modules),
    replicationLinks: (
      refresh ? newEntities.replicationLinks : state.replicationLinks.merge(newEntities.replicationLinks)
    ),
  }
}

const replicationLinksActionsHandler = {
  // Create
  [actionTypes.replicationLinks.createSucceeded]: mergeByFetchingReplicationLinks(false),

  // Fetch
  [actionTypes.replicationLinks.fetchSucceeded]: mergeByFetchingReplicationLinks(true),
}

export default replicationLinksActionsHandler
