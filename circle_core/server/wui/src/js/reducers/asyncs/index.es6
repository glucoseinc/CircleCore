import {handleActions} from 'redux-actions'

import ccInfoActionsHandler from './ccInfo'
import invitationActionsHandler from './invitation'
import moduleActionsHandler from './module'
import replicationLinkActionsHandler from './replicationLink'
import schemaActionsHandler from './schema'
import schemaPropertyTypeActionsHandler from './schemaPropertyType'
import userActionsHandler from './user'


const initialState = {
  isCcInfoFetching: false,
  isCcInfoUpdating: false,

  isInvitationCreating: false,
  isInvitationFetching: false,
  isInvitationDeleting: false,

  isModuleCreating: false,
  isModuleFetching: false,
  isModuleUpdating: false,
  isModuleDeleting: false,

  isReplicationLinkCreating: false,
  isReplicationLinkFetching: false,

  isSchemaCreating: false,
  isSchemaFetching: false,
  isSchemaDeleting: false,

  isSchemaPropertyTypeFetching: false,

  isUserCreating: false,
  isUserFetching: false,
  isUserUpdating: false,
  isUserDeleting: false,
}


const asyncs = handleActions({
  ...ccInfoActionsHandler,
  ...invitationActionsHandler,
  ...moduleActionsHandler,
  ...replicationLinkActionsHandler,
  ...schemaActionsHandler,
  ...schemaPropertyTypeActionsHandler,
  ...userActionsHandler,
}, initialState)

export default asyncs
