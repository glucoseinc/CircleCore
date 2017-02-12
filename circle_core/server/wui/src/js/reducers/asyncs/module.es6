import {actionTypes} from 'src/actions'

import {changeFlagAction} from './utils'


const ccInfoActionsHandler = {
  // Create
  [actionTypes.module.createRequest]: changeFlagAction('isModuleCreating', true),
  [actionTypes.module.createSucceeded]: changeFlagAction('isModuleCreating', false),
  [actionTypes.module.createFailed]: changeFlagAction('isModuleCreating', false),

  // Fetch
  [actionTypes.module.fetchRequest]: changeFlagAction('isModuleFetching', true),
  [actionTypes.module.fetchSucceeded]: changeFlagAction('isModuleFetching', false),
  [actionTypes.module.fetchFailed]: changeFlagAction('isModuleFetching', false),

  // Fetch all
  [actionTypes.module.fetchAllRequest]: changeFlagAction('isModuleFetching', true),
  [actionTypes.module.fetchAllSucceeded]: changeFlagAction('isModuleFetching', false),
  [actionTypes.module.fetchAllFailed]: changeFlagAction('isModuleFetching', false),

  // Update
  [actionTypes.module.updateRequest]: changeFlagAction('isModuleUpdating', true),
  [actionTypes.module.updateSucceeded]: changeFlagAction('isModuleUpdating', false),
  [actionTypes.module.updateFailed]: changeFlagAction('isModuleUpdating', false),

  // Delete
  [actionTypes.module.deleteRequest]: changeFlagAction('isModuleDeleting', true),
  [actionTypes.module.deleteSucceeded]: changeFlagAction('isModuleDeleting', false),
  [actionTypes.module.deleteFailed]: changeFlagAction('isModuleDeleting', false),
}

export default ccInfoActionsHandler
