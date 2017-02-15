import {handleActions} from 'redux-actions'
import {Map} from 'immutable'

import ccInfoActionsHandler from './ccInfo'
import invitationActionsHandler from './invitation'
import moduleActionsHandler from './module'
import replicationLinkActionsHandler from './replicationLink'
import schemaActionsHandler from './schema'
import schemaPropertyTypeActionsHandler from './schemaPropertyType'
import userActionsHandler from './user'

const initialState = {
  ccInfos: new Map(),
  invitations: new Map(),
  messageBoxes: new Map(),
  modules: new Map(),
  myID: null,  // 自分のUserオブジェクトのuuid
  replicationLinks: new Map(),
  schemas: new Map(),
  schemaPropertyTypes: new Map(),
  users: new Map(),
}


const entities = handleActions({
  ...ccInfoActionsHandler,
  ...invitationActionsHandler,
  ...moduleActionsHandler,
  ...replicationLinkActionsHandler,
  ...schemaActionsHandler,
  ...schemaPropertyTypeActionsHandler,
  ...userActionsHandler,
}, initialState)

export default entities
