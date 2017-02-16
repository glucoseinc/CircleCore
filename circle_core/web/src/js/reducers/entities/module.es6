import {actionTypes} from 'src/actions'

import {getNewEntities} from './utils'


const mergeModules = (state, action) => {
  const {
    modules,
    schemas,
  } = getNewEntities(action.payload)
  return {
    ...state,
    modules: state.modules.merge(modules),
    schemas: state.schemas.merge(schemas),
  }
}

const refreshModules = (state, action) => {
  const {
    modules,
    schemas,
  } = getNewEntities(action.payload)
  return {
    ...state,
    modules,
    schemas: state.schemas.merge(schemas),
  }
}

const deleteModules = (state, action) => {
  const {
    modules,
  } = getNewEntities(action.payload)
  return {
    ...state,
    modules: state.modules.filterNot((module, moduleId) => modules.keySeq().includes(moduleId)),
  }
}


const moduleActionsHandler = {
  // Create
  [actionTypes.module.createSucceeded]: mergeModules,

  // Fetch
  [actionTypes.module.fetchSucceeded]: mergeModules,

  // Fetch all
  [actionTypes.module.fetchAllSucceeded]: refreshModules,

  // Update
  [actionTypes.module.updateSucceeded]: mergeModules,

  // Delete
  [actionTypes.module.deleteSucceeded]: deleteModules,
}

export default moduleActionsHandler
