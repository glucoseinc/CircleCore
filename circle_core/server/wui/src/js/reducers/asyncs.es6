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

  isschemaPropertyTypeFetching: false,

  isUserCreating: false,
  isUserFetching: false,
  isUserUpdating: false,
  isUserDeleting: false,

  isInvitationsFetching: false,

  isCcInfoFetching: false,
  isCcInfoUpdating: false,

  isReplicationLinkCreating: false,
  isReplicationLinkFetching: false,
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


  // Fetch Schema property type
  [actionTypes.schemaPropertyType.fetchAllRequest]: changeFlagAction('isschemaPropertyTypeFetching', true),
  [actionTypes.schemaPropertyType.fetchAllSucceeded]: changeFlagAction('isschemaPropertyTypeFetching', false),
  [actionTypes.schemaPropertyType.fetchAllFailed]: changeFlagAction('isschemaPropertyTypeFetching', false),


  // Fetch Invitations
  [actionTypes.invitations.fetchRequest]: changeFlagAction('isInvitationsFetching', true),
  [actionTypes.invitations.fetchComplete]: changeFlagAction('isInvitationsFetching', false),


  // Fetch CcInfo
  [actionTypes.ccInfo.fetchAllRequest]: changeFlagAction('isCcInfoFetching', true),
  [actionTypes.ccInfo.fetchAllSucceeded]: changeFlagAction('isCcInfoFetching', false),
  [actionTypes.ccInfo.fetchAllFailed]: changeFlagAction('isCcInfoFetching', false),
  [actionTypes.ccInfo.fetchMyselfRequest]: changeFlagAction('isCcInfoFetching', true),
  [actionTypes.ccInfo.fetchMyselfSucceeded]: changeFlagAction('isCcInfoFetching', false),
  [actionTypes.ccInfo.fetchMyselfFailed]: changeFlagAction('isCcInfoFetching', false),
  // Update CcInfo
  [actionTypes.ccInfo.updateRequest]: changeFlagAction('isCcInfoUpdating', true),
  [actionTypes.ccInfo.updateSucceeded]: changeFlagAction('isCcInfoUpdating', false),
  [actionTypes.ccInfo.updateFailed]: changeFlagAction('isCcInfoUpdating', false),


  // Create ReplicationLinks
  [actionTypes.replicationLink.createRequest]: changeFlagAction('isReplicationLinkCreating', true),
  [actionTypes.replicationLink.createSucceeded]: changeFlagAction('isReplicationLinkCreating', false),
  [actionTypes.replicationLink.createFailed]: changeFlagAction('isReplicationLinkCreating', false),
  // Fetch ReplicationLinks
  [actionTypes.replicationLink.fetchAllRequest]: changeFlagAction('isReplicationLinkFetching', true),
  [actionTypes.replicationLink.fetchAllSucceeded]: changeFlagAction('isReplicationLinkFetching', false),
  [actionTypes.replicationLink.fetchAllFailed]: changeFlagAction('isReplicationLinkFetching', false),


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
