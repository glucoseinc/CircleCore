import {handleActions} from 'redux-actions'

import {actionTypes} from 'src/actions'


const initialState = {
  isModuleCreating: false,
  isModuleFetching: false,
  isModuleUpdating: false,
  isModuleDeleting: false,

  isSchemaCreating: false,
  isSchemaFetching: false,
  isSchemaDeleting: false,

  isSchemaPropertyTypesFetching: false,

  isUserCreating: false,
  isUserFetching: false,
  isUserUpdating: false,
  isUserDeleting: false,

  isInvitationsFetching: false,

  isCcInfosFetching: false,
  isCcInfosUpdating: false,

  isReplicationLinksCreating: false,
  isReplicationLinksFetching: false,
}


/**
 * 固定ステートに固定値をいれるActionのReducer
 * @param {str} stateName
 * @param {Object} newState
 * @return {Object} 新しいstate
 */
function changeFlagAction(stateName, newState) {
  return (state, action) => {
    let up = {}
    up[stateName] = newState
    return Object.assign({}, state, up)
  }
}

const setSchemaPropertyTypesFetching = (newState) => (state, action) => ({
  ...state,
  isSchemaPropertyTypesFetching: newState,
})


const asyncs = handleActions({
  // Create Module
  [actionTypes.module.createRequest]: changeFlagAction('isModuleCreating', true),
  [actionTypes.module.createSucceeded]: changeFlagAction('isModuleCreating', false),
  [actionTypes.module.createFailed]: changeFlagAction('isModuleCreating', false),
  // Fetch Module
  [actionTypes.module.fetchRequest]: changeFlagAction('isModuleFetching', true),
  [actionTypes.module.fetchSucceeded]: changeFlagAction('isModuleFetching', false),
  [actionTypes.module.fetchFailed]: changeFlagAction('isModuleFetching', false),
  [actionTypes.module.fetchAllRequest]: changeFlagAction('isModuleFetching', true),
  [actionTypes.module.fetchAllSucceeded]: changeFlagAction('isModuleFetching', false),
  [actionTypes.module.fetchAllFailed]: changeFlagAction('isModuleFetching', false),
  // Update Module
  [actionTypes.module.updateRequest]: changeFlagAction('isModuleUpdating', true),
  [actionTypes.module.updateSucceeded]: changeFlagAction('isModuleUpdating', false),
  [actionTypes.module.updateFailed]: changeFlagAction('isModuleUpdating', false),
  // Delete Module
  [actionTypes.module.deleteRequest]: changeFlagAction('isModuleDeleting', true),
  [actionTypes.module.deleteSucceeded]: changeFlagAction('isModuleDeleting', false),
  [actionTypes.module.deleteFailed]: changeFlagAction('isModuleDeleting', false),


  // Create Schema
  [actionTypes.schema.createRequest]: changeFlagAction('isSchemaCreating', true),
  [actionTypes.schema.createSucceeded]: changeFlagAction('isSchemaCreating', false),
  [actionTypes.schema.createFailed]: changeFlagAction('isSchemaCreating', false),
  // Fetch Schema
  [actionTypes.schema.fetchRequest]: changeFlagAction('isSchemaFetching', true),
  [actionTypes.schema.fetchSucceeded]: changeFlagAction('isSchemaFetching', false),
  [actionTypes.schema.fetchFailed]: changeFlagAction('isSchemaFetching', false),
  [actionTypes.schema.fetchAllRequest]: changeFlagAction('isSchemaFetching', true),
  [actionTypes.schema.fetchAllSucceeded]: changeFlagAction('isSchemaFetching', false),
  [actionTypes.schema.fetchAllFailed]: changeFlagAction('isSchemaFetching', false),
  // Delete Schema
  [actionTypes.schema.deleteRequest]: changeFlagAction('isSchemaDeleting', true),
  [actionTypes.schema.deleteSucceeded]: changeFlagAction('isSchemaDeleting', false),
  [actionTypes.schema.deleteFailed]: changeFlagAction('isSchemaDeleting', false),


  // Fetch Schema property types
  [actionTypes.schemaPropertyTypes.fetchRequest]: setSchemaPropertyTypesFetching(true),
  [actionTypes.schemaPropertyTypes.fetchSucceeded]: setSchemaPropertyTypesFetching(false),
  [actionTypes.schemaPropertyTypes.fetchFailed]: setSchemaPropertyTypesFetching(false),


  // Fetch Invitations
  [actionTypes.invitations.fetchRequest]: changeFlagAction('isInvitationsFetching', true),
  [actionTypes.invitations.fetchComplete]: changeFlagAction('isInvitationsFetching', false),

  // Fetch CcInfos
  [actionTypes.ccInfos.fetchRequest]: changeFlagAction('isCcInfosFetching', true),
  [actionTypes.ccInfos.fetchSucceeded]: changeFlagAction('isCcInfosFetching', false),
  [actionTypes.ccInfos.fetchFailed]: changeFlagAction('isCcInfosFetching', false),

  [actionTypes.ccInfos.fetchMyselfRequest]: changeFlagAction('isCcInfosFetching', true),
  [actionTypes.ccInfos.fetchMyselfSucceeded]: changeFlagAction('isCcInfosFetching', false),
  [actionTypes.ccInfos.fetchMyselfFailed]: changeFlagAction('isCcInfosFetching', false),

  // Update CcInfos
  [actionTypes.ccInfos.updateRequest]: changeFlagAction('isCcInfosUpdating', true),
  [actionTypes.ccInfos.updateSucceeded]: changeFlagAction('isCcInfosUpdating', false),
  [actionTypes.ccInfos.updateFailed]: changeFlagAction('isCcInfosUpdating', false),

  // Create replicationLinks
  [actionTypes.replicationLinks.createRequest]: changeFlagAction('isReplicationLinksCreating', true),
  [actionTypes.replicationLinks.createSucceeded]: changeFlagAction('isReplicationLinksCreating', false),
  [actionTypes.replicationLinks.createFailed]: changeFlagAction('isReplicationLinksCreating', false),

  // Fetch replicationLinks
  [actionTypes.replicationLinks.fetchRequest]: changeFlagAction('isReplicationLinksFetching', true),
  [actionTypes.replicationLinks.fetchSucceeded]: changeFlagAction('isReplicationLinksFetching', false),
  [actionTypes.replicationLinks.fetchFailed]: changeFlagAction('isReplicationLinksFetching', false),


  // Create User
  [actionTypes.user.createRequest]: changeFlagAction('isUserCreating', true),
  [actionTypes.user.createSucceeded]: changeFlagAction('isUserCreating', false),
  [actionTypes.user.createFailed]: changeFlagAction('isUserCreating', false),
  // Fetch User
  [actionTypes.user.fetchRequest]: changeFlagAction('isUserFetching', true),
  [actionTypes.user.fetchSucceeded]: changeFlagAction('isUserFetching', false),
  [actionTypes.user.fetchFailed]: changeFlagAction('isUserFetching', false),
  [actionTypes.user.fetchAllRequest]: changeFlagAction('isUserFetching', true),
  [actionTypes.user.fetchAllSucceeded]: changeFlagAction('isUserFetching', false),
  [actionTypes.user.fetchAllFailed]: changeFlagAction('isUserFetching', false),
  [actionTypes.user.fetchMyselfRequest]: changeFlagAction('isUserFetching', true),
  [actionTypes.user.fetchMyselfSucceeded]: changeFlagAction('isUserFetching', false),
  [actionTypes.user.fetchMyselfFailed]: changeFlagAction('isUserFetching', false),
  // Update User
  [actionTypes.user.updateRequest]: changeFlagAction('isUserUpdating', true),
  [actionTypes.user.updateSucceeded]: changeFlagAction('isUserUpdating', false),
  [actionTypes.user.updateFailed]: changeFlagAction('isUserUpdating', false),
  // Delete User
  [actionTypes.user.deleteRequest]: changeFlagAction('isUserDeleting', true),
  [actionTypes.user.deleteSucceeded]: changeFlagAction('isUserDeleting', false),
  [actionTypes.user.deleteFailed]: changeFlagAction('isUserDeleting', false),

}, initialState)

export default asyncs
