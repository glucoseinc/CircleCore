import {actionTypes} from 'src/actions'

import {changeFlagAction} from './utils'


const userActionsHandler = {
  // Create
  [actionTypes.user.createRequest]: changeFlagAction('isUserCreating', true),
  [actionTypes.user.createSucceeded]: changeFlagAction('isUserCreating', false),
  [actionTypes.user.createFailed]: changeFlagAction('isUserCreating', false),

  // Fetch
  [actionTypes.user.fetchRequest]: changeFlagAction('isUserFetching', true),
  [actionTypes.user.fetchSucceeded]: changeFlagAction('isUserFetching', false),
  [actionTypes.user.fetchFailed]: changeFlagAction('isUserFetching', false),

  // Fetch all
  [actionTypes.user.fetchAllRequest]: changeFlagAction('isUserFetching', true),
  [actionTypes.user.fetchAllSucceeded]: changeFlagAction('isUserFetching', false),
  [actionTypes.user.fetchAllFailed]: changeFlagAction('isUserFetching', false),

  // Fetch myself
  [actionTypes.user.fetchMyselfRequest]: changeFlagAction('isUserFetching', true),
  [actionTypes.user.fetchMyselfSucceeded]: changeFlagAction('isUserFetching', false),
  [actionTypes.user.fetchMyselfFailed]: changeFlagAction('isUserFetching', false),

  // Update
  [actionTypes.user.updateRequest]: changeFlagAction('isUserUpdating', true),
  [actionTypes.user.updateSucceeded]: changeFlagAction('isUserUpdating', false),
  [actionTypes.user.updateFailed]: changeFlagAction('isUserUpdating', false),

  // Delete
  [actionTypes.user.deleteRequest]: changeFlagAction('isUserDeleting', true),
  [actionTypes.user.deleteSucceeded]: changeFlagAction('isUserDeleting', false),
  [actionTypes.user.deleteFailed]: changeFlagAction('isUserDeleting', false),
}

export default userActionsHandler
