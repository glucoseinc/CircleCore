import {actionTypes} from 'src/actions'

import {getNewEntities} from './utils'


const refreshSchemaPropertyTypes = (state, action) => {
  const {
    schemaPropertyTypes,
  } = getNewEntities(action.payload)
  return {
    ...state,
    schemaPropertyTypes,
  }
}

const schemaPropertyTypeActionsHandler = {
  // Fetch all
  [actionTypes.schemaPropertyType.fetchAllSucceeded]: refreshSchemaPropertyTypes,
}

export default schemaPropertyTypeActionsHandler
