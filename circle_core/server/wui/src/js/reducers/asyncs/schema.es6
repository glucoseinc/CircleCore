import {actionTypes} from 'src/actions'

import {changeFlagAction} from './utils'


const schemaActionsHandler = {
  // Create
  [actionTypes.schema.createRequest]: changeFlagAction('isSchemaCreating', true),
  [actionTypes.schema.createSucceeded]: changeFlagAction('isSchemaCreating', false),
  [actionTypes.schema.createFailed]: changeFlagAction('isSchemaCreating', false),

  // Fetch
  [actionTypes.schema.fetchRequest]: changeFlagAction('isSchemaFetching', true),
  [actionTypes.schema.fetchSucceeded]: changeFlagAction('isSchemaFetching', false),
  [actionTypes.schema.fetchFailed]: changeFlagAction('isSchemaFetching', false),

  // Fetch all
  [actionTypes.schema.fetchAllRequest]: changeFlagAction('isSchemaFetching', true),
  [actionTypes.schema.fetchAllSucceeded]: changeFlagAction('isSchemaFetching', false),
  [actionTypes.schema.fetchAllFailed]: changeFlagAction('isSchemaFetching', false),

  // Delete
  [actionTypes.schema.deleteRequest]: changeFlagAction('isSchemaDeleting', true),
  [actionTypes.schema.deleteSucceeded]: changeFlagAction('isSchemaDeleting', false),
  [actionTypes.schema.deleteFailed]: changeFlagAction('isSchemaDeleting', false),
}

export default schemaActionsHandler
