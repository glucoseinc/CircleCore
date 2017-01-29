import {actionTypes} from 'src/actions'

import {getNewEntities} from './utils'


const mergeByFetchingSchemas = (refresh) => (state, action) => {
  const newEntities = getNewEntities(action.payload)
  return {
    ...state,
    schemas: refresh ? newEntities.schemas : state.schemas.merge(newEntities.schemas),
    modules: newEntities.modules.merge(state.modules), // newModules are imperfect
  }
}

const setSchemaPropertyTypes = () => (state, action) => {
  const newEntities = getNewEntities(action.payload)
  return {
    ...state,
    schemaPropertyTypes: newEntities.schemaPropertyTypes, // do not merge
  }
}

const schemasActionsHandler = {
  [actionTypes.schemas.fetchSucceeded]: mergeByFetchingSchemas(true),
  [actionTypes.schema.fetchSucceeded]: mergeByFetchingSchemas(false),
  [actionTypes.schemaPropertyTypes.fetchSucceeded]: setSchemaPropertyTypes(),
}

export default schemasActionsHandler
