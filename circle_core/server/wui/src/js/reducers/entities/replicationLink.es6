import {actionTypes} from 'src/actions'

import {getNewEntities} from './utils'


const mergeReplicationLinks = (state, action) => {
  const {
    replicationLinks,
    ccInfos,
    modules,
    schemas,
  } = getNewEntities(action.payload)
  return {
    ...state,
    replicationLinks: state.replicationLinks.merge(replicationLinks),
    ccInfos: state.ccInfos.merge(ccInfos),
    modules: state.modules.merge(modules),
    schemas: state.schemas.merge(schemas),
  }
}

const refreshReplicationLinks = (state, action) => {
  const {
    replicationLinks,
    ccInfos,
    messageBoxes,
    modules,
    schemas,
  } = getNewEntities(action.payload)

  return {
    ...state,
    replicationLinks,
    messageBoxes,
    ccInfos,
    modules,
    schemas: state.schemas.merge(schemas),
  }
}

const deleteReplicationLinks = (state, action) => {
  const {
    replicationLinks,
  } = getNewEntities(action.payload)
  return {
    ...state,
    replicationLinks: state.replicationLinks.filterNot((replicationLink, replicationLinkId) =>
      replicationLinks.keySeq().includes(replicationLinkId)
    ),
  }
}


const replicationLinksActionsHandler = {
  // Create
  [actionTypes.replicationLink.createSucceeded]: mergeReplicationLinks,

  // Fetch all
  [actionTypes.replicationLink.fetchAllSucceeded]: refreshReplicationLinks,

  // Delete
  [actionTypes.replicationLink.deleteSucceeded]: deleteReplicationLinks,
}

export default replicationLinksActionsHandler
