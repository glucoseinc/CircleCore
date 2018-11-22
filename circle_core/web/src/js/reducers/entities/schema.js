import {actionTypes} from 'src/actions'

import {getNewEntities} from './utils'


const mergeSchemas = (state, action) => {
  const {
    schemas,
    modules,
  } = getNewEntities(action.payload)
  return {
    ...state,
    schemas: state.schemas.merge(schemas),
    modules: modules.merge(state.modules), // new modules are imperfect
  }
}

const refreshSchemas = (state, action) => {
  const {
    schemas,
    modules,
  } = getNewEntities(action.payload)
  return {
    ...state,
    schemas,
    modules: modules.merge(state.modules), // new modules are imperfect
  }
}

const deleteSchemas = (state, action) => {
  const {
    schemas,
  } = getNewEntities(action.payload)
  return {
    ...state,
    schemas: state.schemas.filterNot((schema, schemaId) => schemas.keySeq().includes(schemaId)),
  }
}


const schemaActionsHandler = {
  // Create
  [actionTypes.schema.createSucceeded]: mergeSchemas,

  // Fetch
  [actionTypes.schema.fetchSucceeded]: mergeSchemas,

  // Fetch all
  [actionTypes.schema.fetchAllSucceeded]: refreshSchemas,

  // Delete
  [actionTypes.schema.deleteSucceeded]: deleteSchemas,
}

export default schemaActionsHandler
