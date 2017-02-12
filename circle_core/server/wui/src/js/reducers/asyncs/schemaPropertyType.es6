import {actionTypes} from 'src/actions'

import {changeFlagAction} from './utils'


const schemaPropertyTypeActionsHandler = {
  // Fetch all
  [actionTypes.schemaPropertyType.fetchAllRequest]: changeFlagAction('isSchemaPropertyTypeFetching', true),
  [actionTypes.schemaPropertyType.fetchAllSucceeded]: changeFlagAction('isSchemaPropertyTypeFetching', false),
  [actionTypes.schemaPropertyType.fetchAllFailed]: changeFlagAction('isSchemaPropertyTypeFetching', false),
}

export default schemaPropertyTypeActionsHandler
